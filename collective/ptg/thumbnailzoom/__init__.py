from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from collective.plonetruegallery.browser.views.display import \
    BatchingDisplayType
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema

_ = MessageFactory('collective.ptg.thumbnailzoom')

class IThumbnailzoomDisplaySettings(IBaseSettings):
    thumbnailzoom_columns = schema.Int(
        title=_(u"label_thumbnailzoom_columns",
            default=u"Number of thumbs before a forced new row (use a high "
                    u"number if you dont want this)"),
        default=3,
        min=1)
    thumbnailzoom_increase = schema.Int(
        title=_(u"label_thumbnailzoom_increase",
            default=u"Pixels to zoom when mouse over"),
        default=50)
    thumbnailzoom_effectduration = schema.Int(
        title=_(u"label_thumbnaizoom_effectduration",
            default=u"How long time the effect takes"),
        default=100,
        min=16)
    thumbnailzoom_use_icons = schema.Bool(
        title=_(u"label_thumbnailzoom_use_images",
            default=u"Use Image size instead of Thumbnail size"),
        default=False)


class ThumbnailzoomDisplayType(BatchingDisplayType):
    name = u"thumbnailzoom"
    schema = IThumbnailzoomDisplaySettings
    description = _(u"label_thumbnailzoom_display_type",
        default=u"Thumbnailzoom")

    def javascript(self):
        return u"""
<script type="text/javascript" charset="utf-8">
$(window).load(function(){
    //set and get some variables
    var thumbnail = {
        imgIncrease : %(increase)i,
        effectDuration : %(effectduration)i,
        imgWidth : $('.thumbnailWrapper ul li').find('img').width(),
        imgHeight : $('.thumbnailWrapper ul li').find('img').height()
    };

    //make the list items same size as the images
    $('.thumbnailWrapper ul li').css({
        'width' : thumbnail.imgWidth,
        'height' : thumbnail.imgHeight
    });

    //when mouse over the list item...
    $('.thumbnailWrapper ul li').hover(function(){
        $(this).find('img').stop().animate({
            /* increase the image width for the zoom effect*/
            width: parseInt(thumbnail.imgWidth) + thumbnail.imgIncrease,
            /* we need to change the left and top position in order to
            have the zoom effect, so we are moving them to a negative
            position of the half of the imgIncrease */
            left: thumbnail.imgIncrease/2*(-1),
            top: thumbnail.imgIncrease/2*(-1)
        },{
            "duration": thumbnail.effectDuration,
            "queue": false
        });
        //show the caption using slideDown event
        $(this).find('.caption:not(:animated)').slideDown(
            thumbnail.effectDuration);
    //when mouse leave...
    }, function(){
        //find the image and animate it...
        $(this).find('img').animate({
            /* get it back to original size (zoom out) */
            width: thumbnail.imgWidth,
            /* get left and top positions back to normal */
            left: 0,
            top: 0
        }, thumbnail.effectDuration);
        //hide the caption using slideUp event
        $(this).find('.caption').slideUp(thumbnail.effectDuration);
    });
});
</script>
""" % {
    'increase': self.settings.thumbnailzoom_increase,
    'effectduration': self.settings.thumbnailzoom_effectduration,
}

    def css(self):
        style = '%s/++resource++ptg.thumbnailzoom/style.css' % (
            self.portal_url)

        return u"""
<link rel="stylesheet" type="text/css" href="%s"/>
""" % style
ThumbnailzoomSettings = createSettingsFactory(ThumbnailzoomDisplayType.schema)