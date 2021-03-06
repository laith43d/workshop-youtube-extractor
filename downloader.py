"""
    1. Youtube extractor
    2. Extract Video ID and Video Title
    3. Extract Playlists
    4. Extract audio
    5. Multiple bitrate download
    6. Multiple quality download
"""

"""YoutubeDL class.

 YoutubeDL objects are the ones responsible of downloading the
 actual video file and writing it to disk if the user has requested
 it, among some other tasks. In most cases there should be one per
 program. As, given a video URL, the downloader doesn't know how to
 extract all the needed information, task that InfoExtractors do, it
 has to pass the URL to one of them.

 For this, YoutubeDL objects have a method that allows
 InfoExtractors to be registered in a given order. When it is passed
 a URL, the YoutubeDL object handles it to the first InfoExtractor it
 finds that reports being able to handle it. The InfoExtractor extracts
 all the information about the video or videos the URL refers to, and
 YoutubeDL process the extracted information, possibly using a File
 Downloader to download the video.

 YoutubeDL objects accept a lot of parameters. In order not to saturate
 the object constructor with arguments, it receives a dictionary of
 options instead. These options are available through the params
 attribute for the InfoExtractors to use. The YoutubeDL also
 registers itself as the downloader in charge for the InfoExtractors
 that are added to it, so this is a "mutual registration".

 Available options:

 username:          Username for authentication purposes.
 password:          Password for authentication purposes.
 videopassword:     Password for accessing a video.
 ap_mso:            Adobe Pass multiple-system operator identifier.
 ap_username:       Multiple-system operator account username.
 ap_password:       Multiple-system operator account password.
 usenetrc:          Use netrc for authentication instead.
 verbose:           Print additional info to stdout.
 quiet:             Do not print messages to stdout.
 no_warnings:       Do not print out anything for warnings.
 forceurl:          Force printing final URL.
 forcetitle:        Force printing title.
 forceid:           Force printing ID.
 forcethumbnail:    Force printing thumbnail URL.
 forcedescription:  Force printing description.
 forcefilename:     Force printing final filename.
 forceduration:     Force printing duration.
 forcejson:         Force printing info_dict as JSON.
 dump_single_json:  Force printing the info_dict of the whole playlist
                    (or video) as a single JSON line.
 simulate:          Do not download the video files.
 format:            Video format code. See options.py for more information.
 outtmpl:           Template for output names.
 outtmpl_na_placeholder: Placeholder for unavailable meta fields.
 restrictfilenames: Do not allow "&" and spaces in file names
 ignoreerrors:      Do not stop on download errors.
 force_generic_extractor: Force downloader to use the generic extractor
 nooverwrites:      Prevent overwriting files.
 playliststart:     Playlist item to start at.
 playlistend:       Playlist item to end at.
 playlist_items:    Specific indices of playlist to download.
 playlistreverse:   Download playlist items in reverse order.
 playlistrandom:    Download playlist items in random order.
 matchtitle:        Download only matching titles.
 rejecttitle:       Reject downloads for matching titles.
 logger:            Log messages to a logging.Logger instance.
 logtostderr:       Log messages to stderr instead of stdout.
 writedescription:  Write the video description to a .description file
 writeinfojson:     Write the video description to a .info.json file
 writeannotations:  Write the video annotations to a .annotations.xml file
 writethumbnail:    Write the thumbnail image to a file
 write_all_thumbnails:  Write all thumbnail formats to files
 writesubtitles:    Write the video subtitles to a file
 writeautomaticsub: Write the automatically generated subtitles to a file
 allsubtitles:      Downloads all the subtitles of the video
                    (requires writesubtitles or writeautomaticsub)
 listsubtitles:     Lists all available subtitles for the video
 subtitlesformat:   The format code for subtitles
 subtitleslangs:    List of languages of the subtitles to download
 keepvideo:         Keep the video file after post-processing
 daterange:         A DateRange object, download only if the upload_date is in the range.
 skip_download:     Skip the actual download of the video file
 cachedir:          Location of the cache files in the filesystem.
                    False to disable filesystem cache.
 noplaylist:        Download single video instead of a playlist if in doubt.
 age_limit:         An integer representing the user's age in years.
                    Unsuitable videos for the given age are skipped.
 min_views:         An integer representing the minimum view count the video
                    must have in order to not be skipped.
                    Videos without view count information are always
                    downloaded. None for no limit.
 max_views:         An integer representing the maximum view count.
                    Videos that are more popular than that are not
                    downloaded.
                    Videos without view count information are always
                    downloaded. None for no limit.
 download_archive:  File name of a file where all downloads are recorded.
                    Videos already present in the file are not downloaded
                    again.
 cookiefile:        File name where cookies should be read from and dumped to.
 nocheckcertificate:Do not verify SSL certificates
 prefer_insecure:   Use HTTP instead of HTTPS to retrieve information.
                    At the moment, this is only supported by YouTube.
 proxy:             URL of the proxy server to use
 geo_verification_proxy:  URL of the proxy to use for IP address verification
                    on geo-restricted sites.
 socket_timeout:    Time to wait for unresponsive hosts, in seconds
 bidi_workaround:   Work around buggy terminals without bidirectional text
                    support, using fridibi
 debug_printtraffic:Print out sent and received HTTP traffic
 include_ads:       Download ads as well
 default_search:    Prepend this string if an input url is not valid.
                    'auto' for elaborate guessing
 encoding:          Use this encoding instead of the system-specified.
 extract_flat:      Do not resolve URLs, return the immediate result.
                    Pass in 'in_playlist' to only show this behavior for
                    playlist items.
 postprocessors:    A list of dictionaries, each with an entry
                    * key:  The name of the postprocessor. See
                            youtube_dl/postprocessor/__init__.py for a list.
                    as well as any further keyword arguments for the
                    postprocessor.
 progress_hooks:    A list of functions that get called on download
                    progress, with a dictionary with the entries
                    * status: One of "downloading", "error", or "finished".
                              Check this first and ignore unknown values.

                    If status is one of "downloading", or "finished", the
                    following properties may also be present:
                    * filename: The final filename (always present)
                    * tmpfilename: The filename we're currently writing to
                    * downloaded_bytes: Bytes on disk
                    * total_bytes: Size of the whole file, None if unknown
                    * total_bytes_estimate: Guess of the eventual file size,
                                            None if unavailable.
                    * elapsed: The number of seconds since download started.
                    * eta: The estimated time in seconds, None if unknown
                    * speed: The download speed in bytes/second, None if
                             unknown
                    * fragment_index: The counter of the currently
                                      downloaded video fragment.
                    * fragment_count: The number of fragments (= individual
                                      files that will be merged)

                    Progress hooks are guaranteed to be called at least once
                    (with status "finished") if the download is successful.
 merge_output_format: Extension to use when merging formats.
 fixup:             Automatically correct known faults of the file.
                    One of:
                    - "never": do nothing
                    - "warn": only emit a warning
                    - "detect_or_warn": check whether we can do anything
                                        about it, warn otherwise (default)
 source_address:    Client-side IP address to bind to.
 call_home:         Boolean, true iff we are allowed to contact the
                    youtube-dl servers for debugging.
 sleep_interval:    Number of seconds to sleep before each download when
                    used alone or a lower bound of a range for randomized
                    sleep before each download (minimum possible number
                    of seconds to sleep) when used along with
                    max_sleep_interval.
 max_sleep_interval:Upper bound of a range for randomized sleep before each
                    download (maximum possible number of seconds to sleep).
                    Must only be used along with sleep_interval.
                    Actual sleep time will be a random float from range
                    [sleep_interval; max_sleep_interval].
 listformats:       Print an overview of available video formats and exit.
 list_thumbnails:   Print a table of all thumbnails and exit.
 match_filter:      A function that gets called with the info_dict of
                    every video.
                    If it returns a message, the video is ignored.
                    If it returns None, the video is downloaded.
                    match_filter_func in utils.py is one example for this.
 no_color:          Do not emit color codes in output.
 geo_bypass:        Bypass geographic restriction via faking X-Forwarded-For
                    HTTP header
 geo_bypass_country:
                    Two-letter ISO 3166-2 country code that will be used for
                    explicit geographic restriction bypassing via faking
                    X-Forwarded-For HTTP header
 geo_bypass_ip_block:
                    IP range in CIDR notation that will be used similarly to
                    geo_bypass_country

 The following options determine which downloader is picked:
 external_downloader: Executable of the external downloader to call.
                    None or unset for standard (built-in) downloader.
 hls_prefer_native: Use the native HLS downloader instead of ffmpeg/avconv
                    if True, otherwise use ffmpeg/avconv if False, otherwise
                    use downloader suggested by extractor if None.

 The following parameters are not used by YoutubeDL itself, they are used by
 the downloader (see youtube_dl/downloader/common.py):
 nopart, updatetime, buffersize, ratelimit, min_filesize, max_filesize, test,
 noresizebuffer, retries, continuedl, noprogress, consoletitle,
 xattr_set_filesize, external_downloader_args, hls_use_mpegts,
 http_chunk_size.

 The following options are used by the post processors:
 prefer_ffmpeg:     If False, use avconv instead of ffmpeg if both are available,
                    otherwise prefer ffmpeg.
 ffmpeg_location:   Location of the ffmpeg/avconv binary; either the path
                    to the binary or its containing directory.
 postprocessor_args: A list of additional command-line arguments for the
                     postprocessor.

 The following options are used by the Youtube extractor:
 youtube_include_dash_manifest: If True (default), DASH manifests and related
                     data will be downloaded and processed by extractor.
                     You can reduce network I/O by disabling it if you don't
                     care about DASH.
"""

import youtube_dl

ydl_opts = {
    'ignoreerrors': True,
    'quiet': True,
}

keywords = [
    'yanni',
]

input_file = open("playlists.txt")

with open('output.json', 'a+') as output:
    for pl in input_file:
        print(pl, end='')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            pl_info = ydl.extract_info(pl, download=False)
            for v in pl_info['entries']:
                if not v:
                    continue

                # Keyword filtration
                for kw in keywords:
                    if kw in str(v['title']).lower():
                        print(f'video {v["title"]} has been ignored')
                        continue

                    output.write('\n')
                    output.write(f'ID: {v["id"]} - Title: {v["title"]}')

input_file.close()


'''
    to contact me email me on: L@LZAH.online
'''