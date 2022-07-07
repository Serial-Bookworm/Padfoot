from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils.constants import COLS_TO_SEND_BY_HS_API

from .misc import execute_ffn_search_and_response, get_author_details_ao3, get_author_details_ffn, get_story_dates_cleaned_ao3, get_story_details_from_response_ao3
from .models import HarmonyFicsBlacklist, WEBSITE_CHOICES 

class BlacklistView(APIView):
    """
    View to get all blacklisted fics
    """

    def get(self, request):
        all_blacklisted_stories = HarmonyFicsBlacklist.objects.all().order_by('-votes')

        response = {"all_stories": all_blacklisted_stories}

        return Response(response)


class CreateOrAddBlacklistFic(APIView):
    """
    View to create or add votes to a blacklisted fic
    """

    def get(self, request, story_id):
        print("Got: ", story_id)
        if "FFN" in story_id:
            choice = WEBSITE_CHOICES[0]
        elif "AO3" in story_id:
            choice = WEBSITE_CHOICES[1]
        elif "ID" in story_id:
            story_id = int(story_id[2:])
            # story exists, so add a vote
            try:
                obj = HarmonyFicsBlacklist.objects.get(id=story_id)
                obj.votes = obj.votes + 1
                obj.save()
                return Response({"resp": "200_VOTE_ADDED"})
            except:
                return Response({"resp": "404_WRONG_URL"})
        else:
            return Response({"resp": "404_WRONG_URL"})

        story_id = story_id[3:]
        if HarmonyFicsBlacklist.objects.filter(storyid=story_id).exists():
            # story exists, so add a vote
            obj = HarmonyFicsBlacklist.objects.get(storyid=story_id)
            obj.votes = obj.votes + 1
            obj.save()
            return Response({"resp": "200_VOTE_ADDED"})
        else:
            # story doesn't exist, so add it
            if choice == WEBSITE_CHOICES[0]:
                # FFN
                story_all_fields = execute_ffn_search_and_response(story_id)
                HarmonyFicsBlacklist.objects.create(
                    storyid=story_id,
                    website=choice[0],
                    votes=1,
                    story_name=story_all_fields["title"],
                    author_name=story_all_fields["author_name"],
                )
            else:
                # AO3
                story_all_fields = execute_ffn_search_and_response(story_id)
                HarmonyFicsBlacklist.objects.create(
                    storyid=story_id,
                    website=choice[0],
                    votes=1,
                    story_name=story_all_fields["title"],
                    author_name=story_all_fields["authors"],
                )
            return Response({"resp": "200_STORY_AND_VOTE_ADDED"})


class GetStoryDetailsFfn(APIView):
    """View to get story meta from ffn"""

    def get(self, request, story_id):
        print("Got:", story_id)

        story_all_fields = execute_ffn_search_and_response(story_id)

        # prepare the API response with story details
        story = {
            "link": story_all_fields["link"],
            "thumb_image": story_all_fields["story_image"],
        }
        for key in COLS_TO_SEND_BY_HS_API:
            story[key] = story_all_fields[key]

        # save the story or not, check and save here if needed
        # initiate_save_story(story_all_fields)

        # if story gotten, return it as a response
        if story:
            del story["story_id"]
            return Response(story)
        else:
            return Response("Not found.")


class GetStoryDetailsAo3(APIView):
    """View to get story meta from ao3"""

    def get(self, request, story_id):
        url = f"https://archiveofourown.org/works/{story_id}"
        print(f"Trying url from Ao3 API: {url}")
        story = get_story_details_from_response_ao3(story_id)
        story["link"] = url

        story["date_published"] = get_story_dates_cleaned_ao3(story["date_published"], False)
        story["date_updated"] = get_story_dates_cleaned_ao3(story["date_updated"], False)

        return Response(story)


class GetAuthorProfileDetailsFFN(APIView):
    """View to get author profile info from ffn"""

    def get(self, request, au_id):
        print("Got:", au_id)
        url = f"https://www.fanfiction.net/u/{au_id}"
        au_details_crawl = get_author_details_ffn(url)

        return Response(au_details_crawl)


class GetAuthorProfileDetailsAo3(APIView):
    """View to get author profile info from ao3"""

    def get(self, request, au_username):
        print("Got: ", au_username)
        au_details_crawl = get_author_details_ao3(au_username)

        return Response(au_details_crawl)