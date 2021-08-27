# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2017 AI-TF Team

import re
import string
from codecs import unicode_escape_decode
import urllib.parse as decode

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


# 전처리 클래스 정의(백터화)
class SWC_KDAEOD(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_len = int(self.arg_list[0])
        self.preprocessing_type = str(self.arg_list[1])
        self.http_request_method = {
            'OPTIONS ': 180,
            'GET ': 181,
            'HEAD ': 182,
            'POST ': 183,
            'PUT ': 184,
            'DELETE ': 185,
            'TRACE ': 186,
            'CONNECT ': 187
        }

        self.http_request_ver = {
            'HTTP/1.1': 189,
            'HTTP/1.0': 189
        }

        self.http_header_field = {
            # request header
            'Accept-Charset': 200,
            'Accept-Encoding': 200,
            'Accept-Language': 200,
            'If-Match': 200,
            'If-Modified-Since': 200,
            'If-None-Match': 200,
            'If-Range': 200,
            'If-Unmodified-Since': 200,
            'Max-Forwards': 200,
            'Proxy-Authorization': 200,
            'User-Agent': 200,
            'Accept-Ranges': 201,
            'Proxy-Authenticate': 201,
            'Retry-After': 201,
            'WWW-Authenticate': 201,
            'Content-Encoding': 202,
            'Content-Language': 202,
            'Content-Length': 202,
            'Content-Location': 202,
            'Content-MD5': 202,
            'Content-Range': 202,
            'Content-Type': 202,
            'Transfer-Encoding': 203,
            'Cache-Control': 203,
            'Accept: ': 200,
            'From: ': 200,
            'Host: ': 200,
            'Range: ': 200,
            'Referer: ': 200,
            # response header
            'Age: ': 201,
            'Authorization: ': 201,
            'Location: ': 201,
            'Server: ': 201,
            'Vary: ': 201,
            'Warning: ': 201,
            # enentity header
            'Allow: ': 202,
            'ETag: ': 202,
            'Expires: ': 202,
            'Last-Modified': 202,
            # etc header
            'Connection: ': 203,
            'Date: ': 203,
            'Expect: ': 203,
            'Pragma: ': 203,
            'TE: ': 203,
            'Trailer: ': 203,
            'Upgrade: ': 203,
            'Via: ': 203,
            'dstn_asset_group_cd': 204,
            'dstn_country_code': 205,
            'src_country_code': 206,
            'attacker_info': 207,
            'hacking_type': 208,
            'attack_code': 209,
            'eqp_ip_long': 210,
            'opr_user_nm': 211,
            'parser_key': 212,
            'sniper_id': 213,
            'recv_time': 214,
            'eqp_level': 215,
            'eqp_type': 216,
            'eqp_dt': 217,
            'prtc': 218,
            'kyobobook': 219,
            'inci_prcs_stat_floor:': 220,
            'inci_end_update_yn:': 221,
            'parser_file_name:': 222,
            'normalize_result:': 223,
            'inci_user_email:': 224,
            'inci_network_cd:': 225,
            'inci_prcs_stat:': 226,
            'inci_action_dt:': 227,
            'event_type_cd:': 228,
            'inci_user_fax:': 229,
            'inci_dcl_cont:': 230,
            'network_group:': 231,
            'inci_end_type:': 232,
            'inci_user_tel:': 233,
            'inci_req_cont:': 234,
            'dstn_asset_nm:': 235,
            'inci_cate_cd:': 236,
            'inci_user_id:': 237,
            'inci_user_hp:': 238,
            'inci_open_dt:': 239,
            'inci_user_nm:': 240,
            'dstn_ip_list:': 241,
            'network_type:': 242,
            'inci_eqp_dt:': 243,
            'eqp_ip_list:': 244,
            'inci_upd_dt:': 245,
            'inci_reg_dt:': 246,
            'inci_end_dt:': 247,
            'event_level:': 248,
            'src_ip_list:': 249,
            'provider_dt:': 250,
            'ruleset_id:': 251,
            'inci_title:': 252,
            'model_name:': 253,
            'attack_dir:': 254,
            'log_length:': 255,
            'l_code_nm:': 256,
            'field_val:': 257,
            'm_code_nm:': 258,
            'event_seq:': 259,
            'open_time:': 260,
            'parser_ms:': 261,
            'data_type:': 262,
            'country1:': 263,
            'event_id:': 264,
            'pkt_size:': 265,
            'category:': 266,
            'log_code:': 267,
            'group_id:': 268,
            'inci_no:': 269,
            'inci_dt:': 270,
            'log_key:': 271,
            'rule_no:': 272,
            'rule_nm:': 273,
            'payload:': 274,
            'm_code:': 275,
            'l_code:': 276,
            'ip_ver:': 277,
            'inst2:': 278,
            'port2:': 279,
            'type:': 280,
            'risk:': 281,
            'cnt:': 282
        }

        self.http_response_status_code = {
            r"HTTP/\d\.\d\s1\d{2}": 190,
            r"HTTP/\d\.\d\s2\d{2}": 191,
            r"HTTP/\d\.\d\s3\d{2}": 192,
            r"HTTP/\d\.\d\s4\d{2}": 193,
            r"HTTP/\d\.\d\s5\d{2}": 194
        }
        self.SWtoken = {'document.cookie': 300, 'bash_history': 301, 'etc/passwd': 302, 'javascript :': 303,
                        'path/child': 304, 'objectclass': 305, 'onmouseover': 306, 'phpmyadmin': 307, '# include': 308,
                        'password': 309, '= - craw': 310, 'between': 311, 'commit': 312, 'insert': 313, 'select': 314,
                        'passwd': 315, 'onload': 316, 'mail =': 317, 'alert': 318, 'count': 319, 'shell': 320,
                        'table': 321, 'union': 322, 'upper': 323, 'order': 324, 'where': 325, 'winnt': 326,
                        'url =': 327, 'exec': 328, 'from': 329, 'href': 330, 'into': 331, 'wget': 332, 'curl': 333,
                        'and': 334, 'cmd': 335, '/ c': 336, 'or': 337, '/./.././../windows/repair/sam': 338,
                        '/./.././../winnt/repair/sam': 339, '%2f%2e%2e%2fetc%2fpasswd': 340,
                        'http://s.ardoshanghai.com': 341, '/config/aspcms_config.asp': 342,
                        'WINDOWS/SYSTEM32/CONFIG': 343, '..\\..\\winnt\\win.ini': 344, '/conf/db.properties:': 345,
                        '../../../../': 346, '/....//..../': 347, '/winnt/repair/sam': 348, 'ETC/INET/NETWORK': 349,
                        '//////////': 350, 'sysprepunattended': 351, 'ETC%5CNETWORKS': 352, 'wp-config.php': 353,
                        '/../../tmp': 354, '%2e%2e%2f': 355, 'sysprepunattend': 356, '/ETC/INITTAB': 357,
                        'sysprepsysprep': 358, 'mdmLogUploader': 359, 'ETC\\NETWORKS': 360, 'administrator': 361,
                        'configuration': 362, 'windowsupdate': 363, 'browserconfig': 364, 'server-info': 365,
                        'tomcat-docs': 366, 'phpinfo();': 367, '/config.gz': 368, 'programfiles': 369,
                        'filezillaftp': 370, 'wp-content': 371, 'httpd.conf': 372, 'xmlrpc.php': 373,
                        'apachegroup': 374, 'mercurymail': 375, 'filesystems': 376, 'crosseditor': 377,
                        'wlwmanifest': 378, 'filemanager': 379, 'wp-config': 380, '%2e%2e': 381, 'unattended': 382,
                        'interrupts': 383, 'systeminit': 384, 'wpsettings': 385, 'properties': 386, 'authorized': 387,
                        'fileserver': 388, 'kindeditor': 389, 'SYSTEM32': 390, 'boot.ini': 391, 'wp-login': 392,
                        '/conf.d': 393, 'documents': 394, 'sysconfig': 395, 'filezilla': 396, 'webalizer': 397,
                        'webserver': 398, 'available': 399, 'etcpasswd': 400, 'changelog': 401, 'apachectl': 402,
                        'setupinfo': 403, 'localhost': 404, '_history': 405, 'txt.bak': 406, 'cgi-shl': 407,
                        'cgi-bin': 408, 'web-inf': 409, 'win.ini': 410, 'asp.bak': 411, '%252f': 412, '%252e': 413,
                        'settings': 414, 'software': 415, 'sendmail': 416, 'defaults': 417, 'unattend': 418,
                        'services': 419, 'security': 420, 'sessions': 421, 'explorer': 422, 'weblogic': 423,
                        'hostname': 424, 'appevent': 425, 'secevent': 426, 'appstore': 427, 'metabase': 428,
                        'netsetup': 429, 'logfiles': 430, 'htpasswd': 431, 'wsconfig': 432, 'keystore': 433,
                        'NETWORKS': 434, 'document': 435, 'htaccess': 436, 'ckeditor': 437, 'program': 438,
                        'sysprep': 439, 'windows': 440, 'include': 441, 'library': 442, 'private': 443, 'wwwroot': 444,
                        'inetsrv': 445, 'panther': 446, 'plugins': 447, 'desktop': 448, 'osdlogs': 449, 'drivers': 450,
                        'regback': 451, 'httperr': 452, 'version': 453, 'cmdline': 454, 'profile': 455, 'cpuinfo': 456,
                        'meminfo': 457, 'ftproot': 458, 'notepad': 459, 'phpinfo': 756, 'license': 461, 'default': 462,
                        'environ': 463, 'network': 464, 'history': 465, 'confetc': 466, 'INITTAB': 467, 'samples': 468,
                        'phptool': 469, 'manager': 470, 'apache': 471, 'minint': 472, 'system': 473, 'volume': 474,
                        'config': 475, 'server': 476, 'repair': 477, 'tomcat': 478, 'webdav': 479, 'stable': 480,
                        'htdocs': 481, 'schema': 482, 'vhosts': 483, 'mkuser': 484, 'bashrc': 485, 'mounts': 486,
                        'shadow': 487, 'shells': 488, 'resolv': 489, 'fastab': 490, 'access': 491, 'robots': 492,
                        'aspnet': 493, 'ntuser': 494, 'editor': 495, 'XINETD': 496, '.down': 497, 'mysql': 498,
                        'nginx': 499, 'files': 500, 'users': 501, 'xampp': 502, 'sites': 503, 'httpd': 504,
                        'lampp': 505, 'local': 506, 'group': 507, 'debug': 508, 'extra': 509, 'hosts': 910,
                        'issue': 511, 'fstab': 512, 'login': 513, 'error': 514, 'style': 515, 'admin': 516,
                        'index': 517, 'ports': 518, '.asc': 519, 'proc': 520, 'root': 521, 'home': 522, 'logs': 523,
                        'wamp': 524, 'jeus': 525, 'init': 526, 'lamp': 527, 'data': 528, 'conf': 529, 'grub': 530,
                        'motd': 531, 'boot': 532, 'host': 533, 'temp': 534, 'eula': 535, 'keys': 536, 'bash': 537,
                        'defs': 538, 'html': 539, 'perl': 540, 'etc': 541, 'opt': 542, 'usr': 543, 'var': 544,
                        'log': 545, 'php': 546, 'web': 547, 'inf': 548, 'inc': 549, 'ssh': 550, 'bin': 551, 'iis': 552,
                        'win': 553, 'sam': 554, 'ssl': 555, 'rsa': 556, 'ini': 557, 'txt': 558, 'xml': 559, 'dat': 560,
                        'css': 561, 'cnf': 562, 'exe': 563, 'rtf': 564, 'err': 565, 'bak': 566, 'evt': 567, 'sav': 568,
                        'pub': 569, 'asa': 570, 'asp': 571, 'jsp': 572, 'cgi': 573, 'acf': 574, 'old': 575, 'cat': 576,
                        'tmp': 577, 'wp': 578, 'my': 579, 'id': 580, 'gz': 581, '/.htpasswd': 582, ' /.passwd/': 583,
                        '%252f..%252f..%252f..%252f..%252f': 584, '%2e%2e%2f%2e%2e%2f%65%74%63%2f%68%6f%73%74%73': 585,
                        '%2Fetc%2Fpasswd': 586, '%5c%2e%2e%5c%2e%2e%5c%2e%2e': 587,
                        '%c0%af..%c0%af..%c0%af..%c0%af': 588, '../../../../../../etc//////hosts': 589,
                        '.bash_history': 590, '.jpg??': 591, '.jsp%20': 592, '.jsp.': 593, '.old': 594, '.viminfo': 595,
                        '/%uff0e%uff0e/%uff0e%uff0e/%uff0e%uff0e': 596, '/..%255c..%255c..%255c..%255c': 597,
                        '/.....': 598, '/../..%2Fetc%2F': 599, '/../../../../../../': 600,
                        '/../../../sdata2/cck/webapp/cckhome/WEB-INF/jsp/': 601, '/_vti_inf.html': 602,
                        '/apache/logs/access_log': 603, '/app/cckri/WEB-INF/': 604, '/etc/hosts': 605,
                        '/etc/services': 606, '/httpd.conf': 607, '/httpd/logs/access_log': 608, '/password.txt': 609,
                        '/sdata2/cck/webapp/cckhome/engNew/WEB-INF/jsp/': 610, '/sdata2/cckri/WEB-INF/': 611,
                        '/sdata2/eblaw/WEB-INF/classes/': 612,
                        '/sdata2/ecck/coelec/WEB-INF/classes/res/ccourt/spring/': 613, '/service/': 614,
                        '/service/.ssh/': 615, '/service/jeus7/': 616, '/service/xtractor/config/': 617,
                        '/webconfig.txt.php': 618, '/WEB-INF/web.xml': 619, '/windows/win.ini': 620,
                        '/winnt/win.ini': 621, '/winnt/win.ini%00': 622, '/wp-config': 623, '/wp-config.php': 624,
                        '\\%252e%252e\\%252e%252e\\%252e%252e': 625, 'access.log': 626, 'access_log': 627,
                        'authorized_keys': 628, 'bin/id': 629, 'boot.ini%00': 630, 'C:\\': 631,
                        'cat+%2Fetc%2Fpasswd': 632, 'ccklog4j.xml': 633, 'CmdLineAction': 634, 'config.inc.php': 635,
                        'Config.xml': 636, 'configuration.php ': 637, 'context-datasource.xml': 638, 'domain.xml': 639,
                        'error.log': 640, 'etc/./hosts ': 641, 'etc\\shells': 643,
                        'gather.conf': 644, 'index.html': 645, 'index.jsp': 646, 'JeusServer.log': 647,
                        'JeusServer_20200714.log': 648, 'Li4vLi4vLi4vY29uZmIndXJhdGIvbi5waHA=': 649, 'local.xml': 650,
                        'nodes.xml_20170419': 651, 'PARENTDIR': 652, 'Server.xml': 653, 'system.log_09172020': 654,
                        'web.xml': 655, 'WEB-INF/weblogic.xml': 656, 'Windows/system.ini': 657, 'windows/win.ini': 658,
                        'windows/win.ini%00.html ': 659, 'winnt/repair/sam._ ': 660, 'winnt\\win.ini': 661,
                        'Y29uZmIndXJhdGIvbi5waHA=': 662, 'Y29uZmlndXJhdGlvbi5waHA=': 663, 'ZXRjL3Bhc3N3ZA': 664,
                        '/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php': 665,
                        'PD9waHAgQGFzc2VydCgkX1BPU1RbJ2NtZCddKTs/Pg==': 666,
                        'PD9waHAgZXZhbCgkX1BPU1RbeGlhb10pPz54YnNoZWxs': 667,
                        '/fckeditor/editor/filemanager/connectors': 668, 'ZGllKG1kNSgnSGVsbG9waHBTdHVkeScpKTs=': 669,
                        '72C24DD5-D70A-438B-8A42-98424B88AFB8': 670, '_zb_path=../../../../../etc/services': 671,
                        '/remotehtmlview.php?phpAds_path=': 672, '/plugin.php?PHORUMsettings_dir,': 673,
                        'QGV2YWwoJF9QT1NUWydjbWQnXSk7': 674, 'api.backend-app.com:8880': 675,
                        '/connector.minimal.php': 676, '=?US-ASCII?Q?id.txt?=': 677, 'request.getParameter': 678,
                        'thumb.php?src=http': 679, '/wp-file-manager': 680, 'jsp File Browser': 681,
                        'ile_put_contents': 682, '/?gf_page=upload': 683, ' /administrator/': 684,
                        'ru24postwebshell': 685, '?gf_page=upload': 686, 'popupmanagefile': 687, 'seko.vipers.pw': 688,
                        'processbuilder': 689, 'executecommand': 690, 'createtextfile': 691, 'xiangxilianjie': 692,
                        'xpx5fcmdshells': 693, 'WScript.Shell': 694, '/template.php': 695, '/r57shell.php': 696,
                        '/jsspwned.php': 697, 'ExecuteGlobal': 698, 'phpremoteview': 699, 'aspyqanalyser': 700,
                        'base64decoder': 701, 'aXBjb25maWc=': 702, 'gpkiresponse': 703, 'fileuploader': 704,
                        'decodebuffer': 705, 'createobject': 706, 'pentest.jsp': 707, '/wp-content': 708,
                        'uploadimage': 709, 'jspwebshell': 710, 'kcwebtelnet': 711, 'phpwebshell': 712,
                        'bythehacker': 713, 'kingdefacer': 714, 'c99madshell': 715, 'SemrushBot': 716,
                        'downloader': 717, 'Bittorrent': 718, 'htmlencode': 719, 'sqlrootkit': 720, 'shell.php': 721,
                        'cacls.exe': 722, 'popupfile': 723, 'gzinflate': 724, 'nullshell': 725, 'rootshell': 726,
                        '.jsp;.jpg': 727, '.asp;.jpg': 728, 'pastebin': 729, 'nslookup': 730, 'encoding': 731,
                        'response': 732, 'vbscript': 733, 'realpath': 734, 'filepath': 735, 'filename': 736,
                        'function': 737, 'passthru': 738, 'wshshell': 739, 'aspshell': 740, 'backdoor': 741,
                        'antichat': 742, 'asmodeus': 743, 'shell_up': 744, '.jpg.asp': 745, 'r57shell': 746,
                        'c99shell': 747, '*%2e%2f*': 748, '*%2f%2f*': 749, '*%2e%2e*': 750, 'adlib/3': 751,
                        'Wscript': 752, 'xbshell': 753, 'request': 754, 'uploads': 755, 'replace': 757, 'runtime': 758,
                        'execute': 759, 'command': 760, 'myshell': 761, 'hackart': 762, 'entrika': 763, 'aspxspy': 764,
                        'perlkit': 765, 'zorback': 766, 'jsp.jpg': 767, 'ftp://': 768, 'Ka0tic': 769, 'hotlog': 770,
                        'sqlcmd': 771, 'upfile': 772, 'upload': 773, 'action': 774, 'getenv': 775, 'mkdirs': 776,
                        'decode': 777, 'jspspy': 778, 'azrail': 779, 'base64': 780, '.js%70': 781, 'Yeti/': 782,
                        '.htm?': 783, '@eval': 784, 'title': 785, 'unzip': 786, 'uname': 787, 'execl': 788,
                        'popen': 789, 'knull': 790, '<?php': 791, 'h4ntu': 792, 'h4x0r': 793, '.war': 794, 'form': 795,
                        'jpeg': 796, 'aspx': 797, 'name': 798, 'file': 799, 'preg': 800, 'echo': 801, 'eval': 802,
                        'awen': 803, '../*': 804, '%zz': 805, 'chr': 806, 'run': 807, 'get': 808, 'gif': 809,
                        'png': 810, 'zip': 811, 'war': 812, 'cdx': 813, 'rot': 814, 'str': 815, 'r57': 816, 'sh': 817,
                        'zglzcgf0y2hlci5idhrwu2vydmxldfjlc3bvbnnl': 818, 'zglzcgf0y2hlci5idhrwu2vydmxldfjlcxvlc3q': 819,
                        'amf2ys5pby5gawxlt3v0chv0u3ryzwft': 820, 'amf2ys5pby5jbnb1dfn0cmvhbvjlywrlcg': 821,
                        '"javax.servlet.include.request_uri': 822, 'javax.servlet.include.servlet_path': 823,
                        'amf2ys5syw5nllbyb2nlc3ncdwlszgvy': 824, 'javax.servlet.include.path_info"': 825,
                        'amf2ys5pby5cdwzmzxjlzfdyaxrlcg': 826, 'bin/ls%20-al%20/etc|': 827,
                        'javax.servlet.include': 828, 'CONFIGSEARCH_DISP,': 829, 'bin/uname%20-a|': 830,
                        'c2h1dgrvd24g': 831, '/bin/kill -a"': 832, '/namo/manage': 833, '/resin-admin': 834,
                        '+|+dir c:\\': 835, 'bufferedwriter': 836, '&ACTION=CMD': 837, '?ACTION=DIR': 838,
                        '&ACTION=DIR': 839, '/etc/passwd': 840, 'dm1zdgf0ia': 841, 'exec + master': 842,
                        '/configgz': 843, 'dg91y2gg': 844, 'y2hvd24g': 845, 'CMD%20/C': 846, '/bin/sh-': 847,
                        ';system( "': 848, 'y2htb2qg': 849, 'd2hvyw1p': 850, 'dw1hc2sg': 851, 'management': 852,
                        'dispatcher': 853, 'powershell': 854, 'systemroot': 855, 'bhntb2qg': 856, 'dw5hbwug': 857,
                        'cgfzc3dk': 858, 'cm1kaxig': 859, 'y2hncnag': 860, 'c3bsaxqg': 861, 'dg9wic0': 862,
                        'c29ydca': 863, '/bin/ls': 864, 'y2f0ia': 865, 'y2f0pg': 866, 'y3v0ia': 867, '; killall': 868,
                        'd2dldca': 869, 'a2lsbca': 870, 'bw9yzsa': 871, 'z3jlcca': 872, 'wp-json': 873, 'cmd.php': 874,
                        'redirect': 875, 'ognlutil': 876, 'invokeuq': 877, 'ipconfig': 878, 'ifconfig': 879,
                        'bwtkaxig': 880, 'showcase': 881, 'struts 2': 882, ';system': 883, '_PHPLIB': 884,
                        'cm0glq': 885, 'c3uglq': 886, 'invoker': 887, 'netstat': 888, 'exefile': 889, 'soapenv': 890,
                        'xmlsoap': 891, 'appscan': 892, 'Acuneti': 893, 'tcpdump': 894, 'ueditor': 895, 'account': 896,
                        'member': 897, 'spider': 898, 'cookie': 899, 'whoami': 900, ';wget': 901, ';ls -': 902,
                        'y2qg': 903, 'bg4g': 904, 'y3ag': 905, 'd2mg': 906, 'xwork': 907, 'mkdir': 908, 'javax': 909}

    def apply(self, data):
        try:
            data = data.tolist()
        except:
            pass
        try:
            # 1. Replace comma and decode payload
            # print('\nPayload\n', data)
            payload = self._replace_comma_decode(data)
            payload = self._unicode_decode(payload)
            # print('\nReplace comma and decode payload\n', payload)
            # 2. Replace base54, http keywords and special keywords
            payload = self._replace_keywords(payload)
            # print('\nReplace base54, http keywords and special keywords\n', payload)
            # 3. Find all tokens to process
            lpFind = self._tokens(payload)
            # 4. Tokenize with extracted character list
            payload_tokenize = self._tokenize(payload, lpFind)
            # print('\nPayload tokenize\n', payload_tokenize)
            # 5. Tag pre-defined special words with string 'kdbddbdkddbbddkk'
            #   5-1. Remove 'dbdk' string from replacement of keywords
            #   5-2. Replace all tokens
            strTmp = self._specialWords(payload_tokenize, lpFind)
            # print('\nPayload tokenize\n', strTmp)
            # 6. Change characters into ASCII code values
            asciiList = self._asc_code_convert(strTmp)
            # print('\nAscii List\n', asciiList)
            # 7. Add padding data. [00, payload, 00, 255 ... 255]
            resultPayload = self._padding_add(asciiList, self.max_len)
            # Add Scaling between 0 and 1
            for r in range(len(resultPayload)):
                resultPayload[r] = resultPayload[r] / 1000
            return resultPayload

        except Exception as e:
            self.LOGGER.error(e)
            self.LOGGER.error("[Exception] Data_length : {}, RAW_DATA : {}".format(len(data), data))
            self.LOGGER.debug(e, exc_info=True)
            return [1000.] * self.max_len

    def _unicode_decode(self, payload):
        match = re.compile(r"\\u[A-Za-z0-9]{4}")
        temppay = ""
        while (payload != temppay):
            temppay = payload
            key = re.findall(match, payload)
            if key:
                try:
                    payload = payload.replace(key[0], unicode_escape_decode(key[0])[0])
                except:
                    pass

        return payload.encode('utf-8', 'replace').decode('utf-8')

    def _replace_comma_decode(self, payload):
        payload = payload.replace("CCOMMAA", ",")
        temppay = ""
        while (payload != temppay):
            temppay = payload
            payload = decode.unquote(payload)

        return payload

    def _replace_keywords(self, payload):
        payload = payload.lower()
        # Replace http request keyword
        for s in self.http_request_method.keys():
            if payload.find(s.lower()) != -1:
                payload = payload.replace(s.lower(), ' dbdk' + str(self.http_request_method[s]) + 'dbdk ')

        # Replace http response keyword
        for reg in self.http_response_status_code.keys():
            exp = re.compile(reg.lower())
            mat = exp.match(payload)
            if mat:
                payload = payload.replace(mat.group(), ' dbdk' + str(self.http_response_status_code[reg]) + 'dbdk ')

        # Replace http header keyword
        for s in self.http_header_field.keys():
            if payload.find(s.lower()) != -1:
                payload = payload.replace(s.lower(), ' dbdk' + str(self.http_header_field[s]) + 'dbdk ')

        # Replace http request version keyword: This should be the last process.
        for s in self.http_request_ver.keys():
            if payload.find(s.lower()) != -1:
                payload = payload.replace(s.lower(), ' dbdk' + str(self.http_request_ver[s]) + 'dbdk ')
        # Replace special keywords
        for s in self.SWtoken.keys():
            if payload.find(s.lower()) != -1:
                payload = payload.replace(s.lower(), ' dbdk' + str(self.SWtoken[s]) + 'dbdk ')

        return payload

    def _tokens(self, payload):
        lpFind = list(string.punctuation)
        return lpFind

    def _tokenize(self, payload, lpFind):
        try:
            for token in lpFind:
                if token != " ":
                    payload = payload.replace(str(token), ' ' + str(token) + ' ').replace("  ", " ").replace('\r\n',
                                                                                                             '').replace(
                        '\n', '').replace('\r', '').replace('�', '')
            payload = " " + payload + " "
            payload = payload.strip()

            p = re.compile(r'dbdk\s\d\s\d\s\d\sdbdk')
            while True:
                match = p.search(payload)
                if match is not None:
                    s = match.group(0)
                    payload = payload.replace(s, ' ' + s.replace(' ', '') + ' ')
                else:
                    break

            # dbdk_list = p.findall(payload)

            # for d in dbdk_list:
            #     payload = payload.replace(d, d.replace(' ', ''))

            return payload

        except Exception as e:
            self.LOGGER.debug(e, exc_info=True)
            return [1000.] * self.max_len

    def _specialWords(self, payload, lpFind):
        strTemp = ''
        px = re.compile(r'dbdk\d{3}dbdk')
        try:
            resultPayload = payload.split(" ")  # Split by words

            for ChangeWord in resultPayload:
                if ChangeWord == ' ':
                    continue

                # Extract only the characters from RFC2616 replacement strings
                if px.match(ChangeWord):
                    strTemp = strTemp + ' ' + chr(int(ChangeWord[4:-4]))

                elif ChangeWord in lpFind:
                    strTemp = strTemp + " " + ChangeWord

            return strTemp

        except Exception as e:
            self.LOGGER.debug(e, exc_info=True)
            return [1000.] * self.max_len

    def _asc_code_convert(self, strTemp):
        try:
            result = []
            for ch in strTemp:
                if ch != " ":
                    result.append(float(ord(ch)))

            return result

        except Exception as e:
            self.LOGGER.debug(e, exc_info=True)
            return [1000.] * self.max_len

    def _padding_add(self, input_data, max_padd_size):
        iMax = max_padd_size - 4

        payload_ps_len = len(input_data)
        padding0 = []
        padding0.extend([0.] * 2)

        if payload_ps_len < iMax:
            padding1 = [1000.] * (iMax - payload_ps_len)
            input_data = padding0 + input_data + padding1
        else:
            input_data = padding0 + input_data[0:iMax]

        input_data.extend([0.] * 2)

        return input_data
