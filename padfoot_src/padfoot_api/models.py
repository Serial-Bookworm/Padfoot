from django.db import models


WEBSITE_0 = "FFN"
WEBSITE_1 = "AO3"
WEBSITE_CHOICES = (
    (WEBSITE_0, "FFN"),
    (WEBSITE_1, "AO3"),
)

class HarmonyFicsBlacklistModel(models.Model):
    """
    for all dangerous to the heart HHr fics 
    or simply trashy fics that no fan should be subjected to 
    """

    storyid = models.PositiveBigIntegerField(primary_key=True)
    website = models.CharField(
        choices=WEBSITE_CHOICES,
        default=WEBSITE_0,
        max_length=9
    )
    story_name = models.CharField(max_length=512)
    author_name = models.CharField(max_length=512)
    votes = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.storyid + "_" + self.website

    class Meta:
        verbose_name_plural = "Harmony Blacklisted Fics"