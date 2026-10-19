from django.urls import path

from mailing import views
from mailing.views import (MailingCreateView, MailingDeleteView,
                           MailingDetailView, MailingListView,
                           MailingUpdateView, MessageCreateView,
                           MessageDeleteView, MessageDetailView,
                           MessageListView, MessageUpdateView,
                           RecipientCreateView, RecipientDeleteView,
                           RecipientDetailView, RecipientListView,
                           RecipientUpdateView)

app_name = "mailing"

urlpatterns = [
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/create/", RecipientCreateView.as_view(), name="create"),
    path(
        "recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"
    ),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="delete"),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path(
        "messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path(
        "mailings/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailings/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path(
        "mailings/<int:pk>/send/", views.MailingSendView.as_view(), name="mailing_send"
    ),
    path("statistics/", views.UserStatisticsView.as_view(), name="statistics"),
]
