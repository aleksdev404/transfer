from django.urls import path

from . import views


app_name = 'transfer'

urlpatterns = (
    path('', views.HomeView.as_view(), name='home'),
    path('iletisim/', views.ContactView.as_view(), name='contact'),
    path('hakkimizda/', views.AboutView.as_view(), name='about'),
    path('online-siparis/', views.OrderView.as_view(), name='order'),
    path('turlar/', views.TourListView.as_view(), name='tour-list'),
    path('turlar/<int:pk>/', views.TourDetailView.as_view(), name='tour-detail'), # noqa ignore
    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('checkout/<uuid:pk>/', views.TransferExtendedCheckoutView.as_view(), name='transfer-extended-checkout'), # noqa

    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'), # noqa
    path('distance-sales-agreement/', views.DistanceSalesAgreementView.as_view(), name='distance-sales-agreement'), # noqa

    path('test/', views.TestView.as_view(), name='test') # noqa
)
