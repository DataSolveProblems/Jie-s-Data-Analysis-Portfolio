
"""
YouTube Analytics API data model
for more information please visit https://developers.google.com/youtube/analytics/data_model
"""

CoreDimensions = [
	'ageGroup',
	'channel',
	'country',
	'day',
	'gender',
	'month',
	'sharingService',
	'uploaderType',
	'video'
]

SubDimensions = [
	'adType',
	'audienceType',
	'claimedStatus',
	'continent',
	'deviceType',
	'elapsedVideoTimeRatio',
	'group',
	'insightPlaybackLocationType',
	'insightPlaybackLocationDetail',
	'insightTrafficSourceType',
	'insightTrafficSourceDetail',
	'isCurated',
	'liveOrOnDemand',
	'operatingSystem',
	'playlist',
	'province',
	'subscribedStatus',
	'subContinent',
	'youtubeProduct'
]

CoreMetrics = [
	'annotationClickThroughRate',
	'annotationCloseRate',
	'averageViewDuration',
	'comments',
	'dislikes',
	'estimatedMinutesWatched',
	'estimatedRevenue',
	'likes',
	'shares',
	'subscribersGained',
	'subscribersLost',
	'viewerPercentage',
	'views'
]

SubMetrics = [
	'adImpressions',
	'annotationClosableImpressions',
	'annotationCloses',
	'annotationClickableImpressions',
	'annotationClicks',
	'annotationImpressions',
	'audienceWatchRatio',
	'averageTimeInPlaylist',
	'averageViewPercentage',
	'cardImpressions',
	'cardClicks',
	'cardClickRate',
	'cardTeaserImpressions',
	'cardTeaserClicks',
	'cardTeaserClickRate',
	'cpm',
	'estimatedAdRevenue',
	'estimatedRedMinutesWatched',
	'estimatedRedPartnerRevenue ',
	'grossRevenue',
	'monetizedPlaybacks',
	'playbackBasedCpm',
	'playlistStarts',
	'redViews',
	'relativeRetentionPerformance',
	'viewsPerPlaylistStart',
	'videosAddedToPlaylists',
	'videosRemovedFromPlaylists'
]


