from django.urls import path

from api.views import ComponentList, ComponentDetail, ComponentReportList, \
    ComponentReportDetail, WebStoreList, WebStoreDetail, WebStoreComponentList, \
    WebStoreComponentDetail, AssembledConstructionList, AssembledConstructionDetail, \
    ConstructionComponentList, ConstructionComponentDetail, ConstructionReportList, \
    ConstructionReportDetail, UserList, UserDetail, CartList, CartDetail, \
    AppropriateConstructionsForGivenComponents, CartContentGetting, \
    WebShopsForComponent, ConstructionComponents, ComponentConstructions, \
    ComponentReports, ConstructionReports, ComponentsByType, \
    AlmostAppropriateConstructionsForGivenComponents, AdditionUserConstruction, \
    AdditionConstructionReport, AdditionComponentReport, EmptyUserCart, \
    UserConstructionList, ConstructionInstruction, BoughtAssembledConstructionList, \
    TemperatureValue
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('component/', ComponentList.as_view()),
    path('component/<int:pk>/', ComponentDetail.as_view()),
    path('component_report/', ComponentReportList.as_view()),
    path('component_report/<int:pk>/', ComponentReportDetail.as_view()),
    path('web_store/', WebStoreList.as_view()),
    path('web_store/<int:pk>/', WebStoreDetail.as_view()),
    path('webstore_component/', WebStoreComponentList.as_view()),
    path('webstore_component/<int:pk>/', WebStoreComponentDetail.as_view()),
    path('assembled_construction/', AssembledConstructionList.as_view()),
    path('assembled_construction/<int:pk>/', AssembledConstructionDetail.as_view()),
    path('construction_component_pair/', ConstructionComponentList.as_view()),
    path('construction_component_pair/<int:pk>/', ConstructionComponentDetail.as_view()),
    path('construction_report/', ConstructionReportList.as_view()),
    path('construction_report/<int:pk>/', ConstructionReportDetail.as_view()),
    path('user/', UserList.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
    path('cart/', CartList.as_view()),
    path('cart/<int:pk>/', CartDetail.as_view()),
    path('appropriate_construction/', AppropriateConstructionsForGivenComponents.as_view()),
    path('cart_content/', CartContentGetting.as_view()),
    path('empty_cart/', EmptyUserCart.as_view()),
    path('component_shops/<int:pk>/', WebShopsForComponent.as_view()),
    path('construction_component/<int:pk>/', ConstructionComponents.as_view()),
    path('component_construction/<int:pk>/', ComponentConstructions.as_view()),
    path('all_component_reports/<int:pk>/', ComponentReports.as_view()),
    path('all_construction_reports/<int:pk>/', ConstructionReports.as_view()),
    path('almost_appropriate_construction/',
         AlmostAppropriateConstructionsForGivenComponents.as_view()),
    path('components_by_type/', ComponentsByType.as_view()),
    path('add_to_cart/', AdditionUserConstruction.as_view()),
    path('add_report_about_construction/', AdditionConstructionReport.as_view()),
    path('add_report_about_component/', AdditionComponentReport.as_view()),
    path('user_construction_list/', UserConstructionList.as_view()),
    path('user_construction_list/', BoughtAssembledConstructionList.as_view()),
    path('user_construction_list/<int:pk>/', ConstructionInstruction.as_view()),
    path('temperature/', TemperatureValue.as_view()),
]

urlpatterns += staticfiles_urlpatterns()