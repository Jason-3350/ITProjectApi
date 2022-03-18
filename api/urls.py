from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import UserListAPIView, UserDetailAPIView, UserRegister, UserLogin, UserGoals, Recommend, Rewards, UserCoins, UserOrder, Settings, AddGoals, EachRecommend, EachReward

urlpatterns = [
    # 列表视图的路由APIView
    path('users', UserListAPIView.as_view()),
    # 详情视图的路由APIView
    path('users/<int:pk>', UserDetailAPIView.as_view()),

    # 前端发送用户注册请求
    path('register', UserRegister.as_view()),
    # 前端发送用户登录请求
    path('login', UserLogin.as_view()),
    # 前端查询当前用户待办事项
    path('users/<int:pk>/goals', UserGoals.as_view()),
    # 新增待办事项
    path('users/addgoals', AddGoals.as_view()),

    # 前端查询所有推荐奖励
    path('recommend', Recommend.as_view()),
    # 前端查询指定推荐奖励
    path('recommend/<int:pk>', EachRecommend.as_view()),
    # 前端查询所有普通奖励
    path('reward', Rewards.as_view()),
    # 前端查询指定普通奖励
    path('reward/<int:pk>', EachReward.as_view()),

    # 前端查询当前用户订单
    path('order', UserOrder.as_view()),
    # 前端查询当前用户的金币数量
    path('users/<int:pk>/coins', UserCoins.as_view()),

    # 修改密码
    path('settings', Settings.as_view()),

    # token部分
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
