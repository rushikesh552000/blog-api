from django.shortcuts import render, HttpResponse
from rest_framework.views import *
from rest_framework.permissions import *
from .serilizer import *
from rest_framework import generics
# Create your views here.


def find_min_max(page, count):
    page = page - 1
    min_v = int(page) * int(count)
    max_v = int(min_v) + int(count)
    return {'min': min_v, 'max': max_v}


def index(request):
    return HttpResponse('Welcome to post api! 🎉')


class AllPostDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializers_class = PostModelSerializer

    def get(self, request, *args,**kwargs):
        '''
            Returns a list of all posts
             1) pagination with default value 10
             2) FILTERBY title, body, author
        '''

        try:
            page_id = int(request.GET.get('page', 1))
        except:
            page_id = 1

        try:
            limit = int(request.GET.get('limit', 10))
        except:
            limit = 10

        filter_by = request.GET.get('filter_by', '').lower()
        filter_value = request.GET.get('filter_value', '')

        range_v = find_min_max(page_id, limit)
        if filter_by == 'title':
            data_raw_all = PostModel.objects.filter(title__icontains=filter_value, is_show=True)
        elif filter_by == 'author':
            filter_value_multiple = filter_value
            try:
                data_raw_all = PostModel.objects.filter(author__id=filter_value_multiple, is_show=True)
            except:
                data_raw_all = []
        elif filter_by == 'body':
            data_raw_all = PostModel.objects.filter(body__icontains=filter_value, is_show=True)
        else:
            data_raw_all = PostModel.objects.filter(is_show=True)

        data_raw = data_raw_all[range_v['min']:range_v['max']]

        try:
            max_page_counter = int(data_raw_all.count() // limit)+1
        except:
            max_page_counter = 1

        next_link_page_id = page_id + 1
        if page_id == 1:
            previous_page_id = page_id
        else:
            previous_page_id = page_id - 1

        if data_raw:
            st = 200
            msg = 'Data Fetch successfully'
            data = self.serializers_class(data_raw, many=True).data
        else:
            st = 101
            msg = 'No data'
            data = []

        return Response({'status': st, 'message': msg, 'data': data,
                         'current_page':page_id,'max_page_count':max_page_counter,'next_page_id':next_link_page_id,
                         'previous_page_id':previous_page_id,'data_limit':limit,
                         'filter_by':filter_by,'filter_value':filter_value
                         })


    def post(self, request, *args, **kwargs):
        '''
            Allow User to post Single post with parameter of title, body if this paramater is to many we will just use serilizer.valid() method
        '''
        serializer_here = self.serializers_class(data=request.POST)
        if serializer_here.is_valid():
            obj = serializer_here.save()
            st = 200
            msg = 'Post added successfully'
            errors = []
            data = self.serializers_class(obj, many=False).data

        else:
            st = 101
            msg = 'some parameters are required '
            errors = [serializer_here.errors]
            data = {}

        return Response({'status': st, 'message': msg, 'data': data,'errors':errors})


class SinglePostDetailAPI(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializers_class = PostModelSerializer

    def get_queryset(self):
        try:
            post = PostModel.objects.get(author=self.request.user, id=self.kwargs['pk'],is_show=True)
        except Exception as e:
            e.args
            print(e.args)
            post = ''
        return post

    def get(self, request, *args, **kwargs):
        ob = self.get_queryset()
        if ob:
            st = 200
            msg = 'Data Fetch successfully'
            data = self.serializers_class(ob, many=False).data
        else:
            st = 101
            msg = 'No data'
            data = {}

        return Response({'status': st, 'message': msg, 'data': data})

    def put(self, request, *args, **kwargs):
        ob = self.get_queryset()
        errors = []
        data = {}
        if ob:
            serializer = self.serializers_class(instance=ob, data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                st = 200
                msg = 'Post updated successfully'
                errors = []
                data = self.serializers_class(obj, many=False).data
            else:
                st = 101
                msg = 'some required filed'
                errors = [serializer.errors]
        else:
            st = 101
            msg = 'No data'

        return Response({'status': st, 'message': msg, 'data': data, 'errors': errors})

    def delete(self, request, *args, **kwargs):
        ob = self.get_queryset()
        if ob:
            st = 200
            msg = 'Post Deleted successfully'
            ob.is_show = False
            ob.save()
        #     OR we can directly delete object by
        #   ob.delete()
        else:
            st = 101
            msg = 'Post not found'

        return Response({'status': st, 'message': msg})