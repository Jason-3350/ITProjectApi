# Create your views here.

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
# from api.models import User
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Recommendation, Reward, Coins, Goals
from api.serializers import UserSerializer, RecommendSerializer, RewardSerializer, CoinsSerializer, GoalsSerializer


# 允许用户在前端通过用户名和邮箱登录
# 然后在settings里面注册AUTHENTICATION_BACKENDS
class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserListAPIView(APIView):
    # 列表视图
    # permission_classes = [IsAuthenticated, ]

    def get(self, request):
        '''查询所有user接口'''
        # 1. 把所有user查询出来，得到一个查询集
        # 2. 遍历查询集，取出每个模型对象序列化成字典
        # 3. 响应
        qs = User.objects.all()
        serializer = UserSerializer(instance=qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        '''新增'''
        # 获取前端传入的请求json数据并转换成字典
        data = request.data
        # 创建序列化器进行序列化
        serializer = UserSerializer(data=data)
        # 调用序列化器的is_valid方法进行校验
        serializer.is_valid(raise_exception=True)
        # 调用序列化器的save方法进行执行create方法
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(APIView):
    '''详情视图'''

    def get(self, request, pk):
        '''查询指定某个用户的接口'''
        # 获取指定pk的那个模型对象
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 创建序列化器进行序列化
        serializer = UserSerializer(instance=user)
        # 响应
        return Response(serializer.data)

    def put(self, request, pk):
        '''修改指定的用户'''
        # 查询pk所指定的模型对象
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 获取前端传入的请求体数据
        # 创建序列化器进行反序列化
        serializer = UserSerializer(instance=user, data=request.data)
        # 校验
        serializer.is_valid(raise_exception=True)
        # save--->update
        serializer.save()
        # 响应
        return Response(serializer.data)


class UserRegister(APIView):

    def post(self, request):
        '''注册用户'''
        # 获取前端传入的请求json数据并转换成字典{'username':xxx,'userEmail':xxx,'password':xxx}
        data = request.data
        print(data)
        # 获取用户或邮箱并查询模型中是否已经存在
        username = data['username']
        userEmail = data['userEmail']
        try:
            if User.objects.get(username=username) or User.objects.get(email=userEmail):
                return Response({'result': False, 'msg': 'Username or Email is Exist!'})
        except User.DoesNotExist:
            try:
                # 把用户名，密码，邮箱存到数据库
                password = data['password']
                User.objects.create_user(username=username, email=userEmail, password=password)
                return Response({'result': True, 'msg': 'Register Done'})
            except Exception as e:
                print(e)
                return Response({'result': False, 'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)


class UserLogin(APIView):

    def post(self, request):
        '''用户登录'''
        try:
            # 获取前端传入的请求json数据并转换成字典{'username':xxx, 'password':xxx}
            data = request.data
            # 获取前端出来的用户名和密码
            username = data['username']
            password = data['password']
            # 根据用户名验证登录者信息
            user = authenticate(request, username=username, password=password)
            if user:
                serializer = UserSerializer(instance=user)
                # return Response({'result': True, 'msg': 'Login Successfully'})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # 当前登录失败
                return Response({'result': False, 'msg': 'Incorrect username or password !'})
        except Exception as err:
            print(err)
            context = {'result': False, 'msg': str(err)}
            return Response(context)


class UserGoals(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        ''' 用户登录获取所有待办事项 '''
        try:
            # 获取指定pk(user id)的那个模型对象
            qs = Goals.objects.filter(user=pk)
            # 创建序列化器进行序列化
            serializer = GoalsSerializer(instance=qs, many=True)
            # 响应
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response({'result': False, 'msg': str(err)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        '''删除用户指定的goals'''
        # 查询pk所指定的模型对象
        try:
            goal = Goals.objects.get(id=pk)
        except Goals.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddGoals(APIView):

    def post(self, request):
        '''新增待办事项'''
        # goal location date start end status user
        print(request.data)
        try:
            data = request.data
            # 创建序列化器进行序列化
            serializer = GoalsSerializer(data=data)
            # 调用序列化器的is_valid方法进行校验
            serializer.is_valid(raise_exception=True)
            # 调用序列化器的save方法进行执行create方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class Recommend(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request):
        '''查询所有推荐奖励'''
        try:
            # 1. 把所有Recommendation查询出来，得到一个查询集
            qs = Recommendation.objects.all()
            # 2. 遍历查询集，取出每个模型对象序列化成字典
            serializer = RecommendSerializer(instance=qs, many=True)
            # 3. 响应
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        '''添加推荐奖励'''
        try:
            data = request.data
            serializer = RecommendSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class EachRecommend(APIView):

    def get(self, request, pk):
        '''查看指定推荐奖励'''
        try:
            recom = Recommendation.objects.get(id=pk)
            serializer = RecommendSerializer(instance=recom)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class Rewards(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request):
        '''查询所有reward接口'''
        try:
            qs = Reward.objects.all()
            serializer = RewardSerializer(instance=qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        '''添加普通奖励'''
        try:
            data = request.data
            serializer = RewardSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class EachReward(APIView):

    def get(self, request, pk):
        '''查看指定普通奖励'''
        try:
            reward = Reward.objects.get(id=pk)
            serializer = RewardSerializer(instance=reward)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserOrder(APIView):
    # permission_classes = [IsAuthenticated, ]

    pass


class UserCoins(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        ''' 获取当前用户金币数量 '''
        try:
            # 前端传入user id
            coins = Coins.objects.get(user=pk)
            serializer = CoinsSerializer(instance=coins)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class Settings(APIView):

    def post(self, request):
        '''修改密码'''
        try:
            data = request.data
            # 获取前端出来的用户名和密码
            username = data['username']
            oldPassword = data['oldPassword']
            newPassword = data['newPassword']
            # 根据用户名验证登录者信息
            user = authenticate(request, username=username, password=oldPassword)
            if user:
                u = User.objects.get(username=username)
                u.set_password(newPassword)
                u.save()
                return Response(status=status.HTTP_205_RESET_CONTENT)
            else:
                # 当前登录失败
                return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)
