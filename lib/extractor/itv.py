import requests
import re

prodid_re = re.compile("productionId\":\"(.+?)\",")
stream_re  = re.compile("<MediaFiles base=\"(.+?)\"")
format_re  = re.compile("mp4:production/priority/rtmpecatchup/.+?\\.mp4")

srv_url = "http://mercury.itv.com/PlaylistService.svc"
player_url = "https://www.itv.com/mediaplayer/releases/2.13.5/ITVMediaPlayer.swf?v=2.13.5"


def get(url, params=None):
	r = requests.get(url, params=params)
	if r.status_code >= 300:
		raise Exception("Request : '" + url + "' returned: " + str(r.status_code))
	return r.text

def _get_playlist(id):
	body = _soap_msg % id
	headers = {
		"Host":"mercury.itv.com",
		"Referer":"http://www.itv.com/mercury/Mercury_VideoPlayer.swf?v=1.6.479/[[DYNAMIC]]/2",
		"Content-type":"text/xml; charset=utf-8",
		"SOAPAction":"http://tempuri.org/PlaylistService/GetPlaylist"
	}
	r = requests.post(srv_url, data=body, headers=headers)
	if r.status_code >= 300:
		raise Exception("Request : '" + srv_url + "' returned: " + str(r.status_code))
	return r.text

def extract(url):
	page = get(url)

	matches = prodid_re.search(page)
	if not matches or len(matches.groups()) == 0:
		raise Exception("Unable to find production id")
	prodid = matches.group(1).replace('\\', '')

	playlist = _get_playlist(prodid)

	matches = stream_re.search(playlist)
	if not matches or len(matches.groups()) == 0:
        	if "InvalidGeoRegion" in playlist:
			raise Exception("Programme only available in UK")
		else:
			raise Exception("Unable to find rtmpe stream")
	stream = matches.group(1).replace('&amp;', '&')

	formats = format_re.findall(playlist)
	if not formats or len(formats) == 0:
		raise Exception("Unable to find play format")
	# First format is lowest quality and last is highest quality
	quality = formats[len(formats)-1]

	cmd = ['-r', stream, '--swfUrl', player_url, '--playpath', 
					quality, '--swfVfy', player_url]

	return cmd

_soap_msg = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/" xmlns:itv="http://schemas.datacontract.org/2004/07/Itv.BB.Mercury.Common.Types" xmlns:com="http://schemas.itv.com/2009/05/Common">
<soapenv:Header/>
<soapenv:Body>
  <tem:GetPlaylist>
    <tem:request>
      <itv:ProductionId>%s</itv:ProductionId>
        <itv:RequestGuid>FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF</itv:RequestGuid>
        <itv:Vodcrid>
          <com:Id/>
          <com:Partition>itv.com</com:Partition>
      </itv:Vodcrid>
    </tem:request>
    <tem:userInfo>
      <itv:Broadcaster>Itv</itv:Broadcaster>
      <itv:GeoLocationToken>
        <itv:Token/>
      </itv:GeoLocationToken>
      <itv:RevenueScienceValue>ITVPLAYER.12.18.4</itv:RevenueScienceValue>
      <itv:SessionId/>
      <itv:SsoToken/>
      <itv:UserToken/>
    </tem:userInfo>
    <tem:siteInfo>
      <itv:AdvertisingRestriction>None</itv:AdvertisingRestriction>
      <itv:AdvertisingSite>ITV</itv:AdvertisingSite>
      <itv:AdvertisingType>Any</itv:AdvertisingType>
      <itv:Area>ITVPLAYER.VIDEO</itv:Area>
      <itv:Category/>
      <itv:Platform>DotCom</itv:Platform>
      <itv:Site>ItvCom</itv:Site>
    </tem:siteInfo>
    <tem:deviceInfo>
      <itv:ScreenSize>Big</itv:ScreenSize>
    </tem:deviceInfo>
    <tem:playerInfo>
      <itv:Version>2</itv:Version>
    </tem:playerInfo>
  </tem:GetPlaylist>
</soapenv:Body>
</soapenv:Envelope>"""
