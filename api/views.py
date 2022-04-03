# Create your views here.
import urllib.request

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from icalendar import Calendar
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Recommendation, Reward, Coins, Goals, Notices, Order, UserICal
from api.serializers import UserSerializer, RecommendSerializer, RewardSerializer, CoinsSerializer, GoalsSerializer, NoticesSerializer, OrderSerializer, UserICalSerializer


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
                return Response(status=status.HTTP_226_IM_USED)
        except User.DoesNotExist:
            try:
                # 把用户名，密码，邮箱存到数据库
                password = data['password']
                User.objects.create_user(username=username, email=userEmail, password=password)
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_404_NOT_FOUND)


# class UserLogin(APIView):
#
#     def post(self, request):
#         '''用户登录'''
#         try:
#             # 获取前端传入的请求json数据并转换成字典{'username':xxx, 'password':xxx}
#             data = request.data
#             # 获取前端出来的用户名和密码
#             username = data['username']
#             password = data['password']
#             # 根据用户名验证登录者信息
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 serializer = UserSerializer(instance=user)
#                 # return Response({'result': True, 'msg': 'Login Successfully'})
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 # 当前登录失败
#                 return Response({'result': False, 'msg': 'Incorrect username or password !'})
#         except Exception as err:
#             print(err)
#             return Response(status=status.HTTP_404_NOT_FOUND)

class UserInfo(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, uid):
        '''Get user details'''
        try:
            foundUser = User.objects.get(id=uid)
            serializer = UserSerializer(instance=foundUser)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserGoals(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, uid, sdate):
        ''' 用户登录获取所有待办事项 '''
        try:
            # 获取指定pk(user id)的那个模型对象
            qs = Goals.objects.filter(user=uid).filter(date=sdate)
            # 创建序列化器进行序列化
            serializer = GoalsSerializer(instance=qs, many=True)
            # 响应
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class EditUserGoal(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        '''删除用户指定的goals'''
        # 查询pk所指定的模型对象
        try:
            goal = Goals.objects.get(id=pk)
        except Goals.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        try:
            goal = Goals.objects.get(id=pk)
            coinObj = Coins.objects.get(user=goal.user)

            # change into done, add one coin
            if goal.status == 0:
                goal.status = 1
                # add coin for the user
                if coinObj.coin < 0:
                    coinObj.coin = 0
                else:
                    coinObj.coin = coinObj.coin + 1
                    print(coinObj.coin)
            # change into undo, deduct one coin
            else:
                goal.status = 0
                if coinObj.coin - 1 < 0:
                    coinObj.coin = 0
                else:
                    coinObj.coin = coinObj.coin - 1
            coinObj.save()
            goal.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class AddGoals(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        '''新增待办事项'''
        # goal location date start end status user
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
    permission_classes = [IsAuthenticated, ]

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
    permission_classes = [IsAuthenticated, ]

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
    permission_classes = [IsAuthenticated, ]

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
    permission_classes = [IsAuthenticated, ]

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
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        '''获取用户订单信息，这里pk是用户id'''
        try:
            order = Order.objects.filter(user=pk)
            serializer = OrderSerializer(instance=order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)
        pass

    def put(self, request, pk):
        '''删除用户的订单，这里的pk是订单id'''
        try:
            order = Order.objects.get(id=pk)
            order.status = 0
            order.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class AddOrder(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        '''添加用户订单信息'''
        try:
            data = request.data
            serializer = OrderSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserCoins(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, uid):
        ''' 获取当前用户金币数量 '''
        try:
            # 前端传入user id
            coin = Coins.objects.get(user=uid)
            serializer = CoinsSerializer(instance=coin)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uid):
        '''修改当前用户金币数量'''
        try:
            data = request.data
            resCoin = Coins.objects.get(user=uid)
            resCoin.coin = data['newCoin']
            resCoin.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class Settings(APIView):
    permission_classes = [IsAuthenticated, ]

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


class ICalendarURL(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        '''添加iCalendar的url，读取数据后存到数据库'''
        try:
            data = request.data
            user_id = data['user']
            icsUrl = data['icsUrl']
            user = User.objects.get(id=user_id)
            req = urllib.request.urlopen(icsUrl)
            req_data = req.read()
            cal = Calendar.from_ical(req_data)
            icsName = ""
            for event in cal.walk():
                if event.name == "VCALENDAR":
                    icsName = str(event.get('X-WR-CALNAME'))
                    try:
                        UserICal.objects.filter(icsName=icsName)
                        return Response(status=status.HTTP_226_IM_USED)
                    except UserICal.DoesNotExist:
                        continue
                if event.name == "VEVENT":
                    summary = str(event.get('summary'))
                    startDateTime = event.get('dtstart').dt
                    endDateTime = event.get('dtend').dt
                    start_date = startDateTime.date()
                    start_time = startDateTime.time()
                    end_time = endDateTime.time()
                    location = str(event.get('location'))
                    UserICal.objects.create(summary=summary, date=start_date, start=start_time, end=end_time, location=location, icsName=icsName, user=user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class ICalendarFile(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        '''import ics files and save to database'''
        try:
            data = request.data
            up_file = request.FILES['file'].read()
            user_id = data['user']
            # 获取用户名加到文件名后面
            user = User.objects.get(id=user_id)
            gCal = Calendar.from_ical(up_file)
            icsFileName = ""
            for event in gCal.walk():
                if event.name == "VCALENDAR":
                    icsFileName = str(event.get('X-WR-CALNAME'))
                    try:
                        UserICal.objects.filter(icsName=icsFileName)
                        return Response(status=status.HTTP_226_IM_USED)
                    except UserICal.DoesNotExist:
                        continue
                if event.name == "VEVENT":
                    summary = str(event.get('summary'))
                    startDateTime = event.get('dtstart').dt
                    endDateTime = event.get('dtend').dt
                    start_date = startDateTime.date()
                    start_time = startDateTime.time()
                    end_time = endDateTime.time()
                    location = str(event.get('location'))
                    UserICal.objects.create(summary=summary, date=start_date, start=start_time, end=end_time, location=location, icsName=icsFileName, user=user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetLecture(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, uid, sdate):
        ''' 用户指定日期的lecture '''
        try:
            qs = UserICal.objects.filter(user=uid).filter(date=sdate)
            serializer = UserICalSerializer(instance=qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class EditLecture(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk):
        '''修改lecture的status'''
        try:
            lecture = UserICal.objects.get(id=pk)
            coinObj = Coins.objects.get(user=lecture.user)
            # change into done, add one coin
            if lecture.status == 0:
                lecture.status = 1
                # add coin for the user
                if coinObj.coin < 0:
                    coinObj.coin = 0
                else:
                    coinObj.coin = coinObj.coin + 1
                    print(coinObj.coin)
            # change into undo, deduct one coin
            else:
                lecture.status = 0
                if coinObj.coin - 1 < 0:
                    coinObj.coin = 0
                else:
                    coinObj.coin = coinObj.coin - 1
            coinObj.save()
            lecture.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)


class Notice(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, uid):
        try:
            notices = Notices.objects.filter(user=uid)
            serializer = NoticesSerializer(instance=notices, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_404_NOT_FOUND)
