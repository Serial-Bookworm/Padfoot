from django.db import models


WEBSITE_CHOICES = (
    ("0", "FFN"),
    ("1", "AO3"),
)

class HarmonyFicsBlacklist(models.Model):
    """
    for all dangerous to the heart HHr fics 
    or simply trashy fics that no fan should be subjected to 
    """

    storyid = models.CharField(max_length=30)
    website = models.CharField(
        choices=WEBSITE_CHOICES,
        max_length=50,
    )
    story_name = models.CharField(max_length=150)
    author_name = models.CharField(max_length=150)
    votes = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.storyid + "_" + self.website

    class Meta:
        verbose_name_plural = "Harmony Blacklisted Fics"