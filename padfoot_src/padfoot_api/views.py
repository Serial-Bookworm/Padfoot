from email import message
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HarmonyBlacklistFicsSerializer
from rest_framework.generics import ListAPIView

from .utils.constants import COLS_TO_SEND_BY_HS_API

from .misc import execute_ffn_search_and_response, get_author_details_ao3, get_author_details_ffn, get_story_dates_cleaned_ao3, get_story_details_from_response_ao3
from .models import HarmonyFicsBlacklistModel, WEBSITE_CHOICES, Starboard3HModel 


class ShowHarmonyBlacklistView(ListAPIView):
    serializer_class = HarmonyBlacklistFicsSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.order_by('-votes')
    lookup_field = 'storyid'


class CreateOrAddBlacklistFicView(APIView):
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
                obj = HarmonyFicsBlacklistModel.objects.get(id=story_id)
                obj.votes = obj.votes + 1
                obj.save()
                return Response({"resp": "200_VOTE_ADDED"})
            except:
                return Response({"resp": "404_WRONG_URL"})
        else:
            return Response({"resp": "404_WRONG_URL"})
        print("CHOICE = ", choice)
        story_id = story_id[3:]
        if HarmonyFicsBlacklistModel.objects.filter(storyid=story_id).exists():
            # story exists, so add a vote
            obj = HarmonyFicsBlacklistModel.objects.get(storyid=story_id)
            obj.votes = obj.votes + 1
            obj.save()
            return Response({"resp": "200_VOTE_ADDED"})
        else:
            # story doesn't exist, so add it
            if choice == WEBSITE_CHOICES[0]:
                # FFN
                story_all_fields = execute_ffn_search_and_response(story_id)
                HarmonyFicsBlacklistModel.objects.create(
                    storyid=story_id,
                    website=choice[0],
                    votes=1,
                    story_name=story_all_fields["title"],
                    author_name=story_all_fields["author_name"],
                )
            else:
                # AO3
                story_all_fields = get_story_details_from_response_ao3(story_id)
                HarmonyFicsBlacklistModel.objects.create(
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


class StarboardView(APIView):
    """
    View to add or remove a message from starboard table
    """

    def get(self, request):
        response = ""
        payload = request.data
        
        # stars reached count = 2, probably add it to the db table
        if not Starboard3HModel.objects.filter(message_id_orig = payload["message_id"]).exists():
            try:
                Starboard3HModel.objects.create(
                    message_id_orig = payload["message_id"],
                    channel_id_original = payload["channel_id_original"],
                    author_id = payload["author_id"],
                    message_id_sent = payload["message_sent_id"]
                )
                response = "200_STARBOARD_MESSAGE_ADDED"
            except Exception as e:
                print("Exception: ", e)
                response = "500_STARBOARD_ERROR"
        else:
            response = "200_MESSAGE_ALREADY_PRESENT"
    
        return Response({"resp" : response})
