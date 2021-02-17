from django.shortcuts import render,HttpResponse ,Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import WeSerializer, DnSerializer, hosSerializer
from rest_framework.parsers import JSONParser
import requests
import json
from datetime import datetime
import pandas as pd
from django.utils.dateparse import parse_datetime
from .models import *
import numpy as np
from io import BytesIO
import numpy
import base64


import glob
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


def choice(request):
    return render(request,'wan/choice.html')

class Datalist(APIView): #전체 장치 조회

    def post(self, request, format = None):

        serializer = DnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    def get(self,request,format=None):
        a = We.objects.all()
        a.delete()
        b = Dn.objects.all()
        b.delete()
        c = request.GET['api_key']
        d = request.GET['api_secret']
        # print(c,d)
        # api_key = request.GET.get('api_key')
        # api_secret = request.GET.get('api_secret')
        # kind = request.GET('category',None)
        url = 'https://oa.tapaculo365.com/tp365/v1/channel/get_lst'
        params = {
            'search': '',
            'api_key': c,  # 4528458
            'api_secret': d  # '3fa6d40e4461cd250a683b86eed42bad'
        }
        r = requests.get(url, params=params)
        c = r.json()['rows']
        df2 = pd.DataFrame(c)
        #df2 = df2.filter(['device_name', 'device_mac', 'sensor_mac']).drop_duplicates()
        for i in range(len(df2)):
            df2.iloc[i]['device_name'] = df2.iloc[i].device_name + df2.iloc[i].ch_no
        df2 = df2[df2.ch_unit == "℃"]
        df2.drop(columns=['VS_INTERVAL', 'VS_SPLRATE', 'device_splrate', 'battery', 'lqi', 'last_update', 'ch_value',
                         'ch_timestamp'], inplace=True)
        df2.fillna('X',inplace=True)
        for i in range(len(df2)):
            a2 = Dn(device_name=df2.iloc[i].device_name, device_mac=df2.iloc[i].device_mac,
                    sensor_mac=df2.iloc[i].sensor_mac,device_model=df2.iloc[i].device_model,device_interval=df2.iloc[i].device_interval,device_version=df2.iloc[i].device_version,sensor_model=df2.iloc[i].sensor_model,ch_no=df2.iloc[i].ch_no,ch_name=df2.iloc[i].ch_name, id=i + 1)
            a2.save()
        data_list = Dn.objects.all()
        serializer = DnSerializer(data_list,many=True)
        return Response(serializer.data)





class DeviceData(APIView): # 원하는 장치의 이름이 포함된 데이터중 첫번째 장치맥,센서맥으로 장치의 24시간 데이터조회

    def get(self, request, format=None):
        # a = request.GET.get('name')
        # api_key = request.GET.get('api_key')
        # api_secret = request.GET.get('api_secret')
        c = request.GET['api_key']
        d = request.GET['api_secret']
        e = request.GET['device']
        # print(e)

        device_mac = Dn.objects.filter(device_name__contains=e)[0].device_mac
        sensor_mac = Dn.objects.filter(device_name__contains=e)[0].sensor_mac
        url2 = 'https://oa.tapaculo365.com/tp365/v1/channel/get_recentdata'
        params2 = {
            'device_mac': device_mac,
            'sensor_mac': sensor_mac,
            'api_key': c,
            'api_secret': d
        }
        r2 = requests.get(url2, params=params2)
        data = r2.json()
        df = pd.DataFrame(data['rows'])
        df.timestamp = list(
            map(lambda x: datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S'), df.timestamp))
        df = df.replace('NULL','0')
        #df.ch1[df.ch1 == 'NULL'] = 0

        df.ch1 = df.ch1.astype('float')



        for i in range(len(df.ch1)):
            times = parse_datetime(df.timestamp[i])
            a1 = We(time=times, temp=df.ch1[i], id=i + 1)
            a1.save()
        a2 = hos(device_name=Dn.objects.filter(device_name__contains=e)[0].device_name,max_temp=df.ch1.max(),min_temp=df.ch1.min(),mean_temp=df.ch1.mean())
        a2.save()

        device_data = We.objects.all()
        serializer = WeSerializer(device_data, many=True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = WeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TempDevice(APIView):
    def get(self,request,format=None):
        temp = hos.objects.all()
        serializer = hosSerializer(temp,many=True)
        return Response(serializer.data)

# class DeviceDetail(APIView):
#     def get_object(self,pk):
#         try:
#             return We.objects.get(pk=pk)
#         except We.DoseNotExist:
#             raise Http404
#
#     def get(self,request,pk):
#         data = self.get_object(pk)
#         serializer = WeSerializer(data)
#         return Response(serializer.data)

# class Data(APIView): # 하나의 데이터 조회
#     def get_object(self,pk):
#         try:
#             return Dn.objects.get(pk=pk)
#         except Dn.DoesNotExist:
#             raise Http404
#
#     def get(self,request,pk):
#         dataa = self.get_object(pk)
#         serializer = DnSerializer(dataa)
#         return Response(serializer.data)
#
#     def put(self,request,pk,format=None):
#         post=self.get_object(pk)
#         serializer = DnSerializer(post,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,pk,format=None):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
