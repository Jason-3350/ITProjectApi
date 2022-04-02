from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import UserRegister, UserGoals, Recommend, Rewards, UserCoins, Settings, AddGoals, EachRecommend, EachReward, ICalendarFile, \
    ICalendarURL, GetLecture, Notice, AddOrder, UserOrder, EditUserGoal, EditLecture, UserInfo

urlpatterns = [
    # token部分
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # 前端发送用户注册请求
    path('register', UserRegister.as_view()),
    # 前端发送用户登录请求
    # path('login', UserLogin.as_view()),
    path('userinfo/<int:uid>', UserInfo.as_view()),
    # 前端查询当前用户待办事项
    path('goals/<int:uid>/<str:sdate>', UserGoals.as_view()),
    # 新增待办事项
    path('users/addgoals', AddGoals.as_view()),
    # 删除或修改待办事项
    path('users/goals/<int:pk>', EditUserGoal.as_view()),
    # 前端查询所有推荐奖励
    path('recommend', Recommend.as_view()),
    # 前端查询指定推荐奖励
    path('recommend/<int:pk>', EachRecommend.as_view()),
    # 前端查询所有普通奖励
    path('reward', Rewards.as_view()),
    # 前端查询指定普通奖励
    path('reward/<int:pk>', EachReward.as_view()),
    # 查询当前用户订单
    path('users/<int:pk>/order', UserOrder.as_view()),
    # 添加用户的订单
    path('users/addorder', AddOrder.as_view()),
    # 前端查询当前用户的金币数量
    path('users/<int:uid>/coins', UserCoins.as_view()),
    # 修改密码
    path('settings', Settings.as_view()),
    # 保存icalendar url
    path('icalurl', ICalendarURL.as_view()),
    # 保存icalendar文件
    path('icalfile', ICalendarFile.as_view()),
    # 读取icalendar文件
    path('lectures/<int:uid>/<str:sdate>', GetLecture.as_view()),
    # 修改lectures事项
    path('users/lectures/<int:pk>', EditLecture.as_view()),
    # 查询通知
    path('notice/<int:uid>', Notice.as_view()),
]
