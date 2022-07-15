from django.urls import path, re_path, include
from rest_framework import routers

from . import views


urlpatterns = [
    # HHR STORY BLACKLIST PATHS
    path(
        "hhr_blacklist_show/",
        views.ShowHarmonyBlacklistView.as_view(),
        name="hhr_blacklist_show",
    ),
    path(
        "hhr_blacklist_create_or_update/<str:story_id>/",
        views.CreateOrAddBlacklistFicView.as_view(),
        name="hhr_blacklist_add_or_modify",
    ),
    # FFN/AO3 STORY, AUTHOR PATHS
    path(
        "ffn/<str:story_id>/",
        views.GetStoryDetailsFfn.as_view(),
        name="get_storydetails_endpoint_ffn",
    ),
    path(
        "ao3/<str:story_id>/",
        views.GetStoryDetailsAo3.as_view(),
        name="get_storydetails_endpoint_ao3",
    ),
    path(
        "au_ffn_profile/<str:au_id>",
        views.GetAuthorProfileDetailsFFN.as_view(),
        name="get_author_profile_ffn",
    ),
    path(
        "au_ao3_profile/<str:au_username>", 
        views.GetAuthorProfileDetailsAo3.as_view(), 
        name="get_author_profile_ao3"
    ),
    # starboard 3H
    path(
        "starboard3H/",
        views.StarboardView.as_view(),
        name="starboard_3H"
    ),
]
