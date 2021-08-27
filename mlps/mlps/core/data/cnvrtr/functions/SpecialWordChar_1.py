# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2017-2018 AI Core Team, Intelligence R&D Center.

import re
import urllib.parse as decode
from operator import itemgetter

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract

SWupper_arr = [
            ['ZGlzcGF0Y2hlci5IdHRwU2VydmxldFJlcXVlc3Q'],['amF2YS5sYW5nLlByb2Nlc3NCdWlsZGVy'],['amF2YS5pby5JbnB1dFN0cmVhbVJlYWRlcg'],['amF2YS5pby5GaWxlT3V0cHV0U3RyZWFt'],
            ['amF2YS5pby5CdWZmZXJlZFdyaXRlcg'],['ZGlzcGF0Y2hlci5IdHRwU2VydmxldFJlc3BvbnNl'],['aWZjb25maWc'],['bmV0c3RhdCAt'],['cHMgLQ'],['bHNtb2Qg'],['bmV0c3RhdCA'],
            ['ZGYg'],['dGNwZHVtcCA'],['cGVybCA'],['d2dldCA'],['YmFzaCA'],['Y2Qg'],['dm1zdGF0IA'],['bHNvZiA'],['Zgly'],['ZWNobyA'],['bmMgLQ'],['cGluZyA'],['c2h1dGRvd24g'],
            ['a2lsbCA'],['dW5hbWUg'],['cHdk'],['bWtkaXIg'],['cm0gLQ'],['dmkg'],['bXYg'],['Y2htb2Qg'],['dG91Y2gg'],['bHMg'],['Y2F0IA'],['Y2F0Pg'],['c3UgLQ'],['d2hvYW1p'],
            ['dG9wIC0'],['ZGF0ZQ'],['cGFzc3dk'],['c3R0eSA'],['cm1kaXIg'],['bG4g'],['Y3Ag'],['Y2hvd24g'],['Y2hncnAg'],['dW1hc2sg'],['bW9yZSA'],['aGVhZCA'],
            ['dGFpbCA'],['d2Mg'],['Y3V0IA'],['c29ydCA'],['c3BsaXQg'],['Z3JlcCA'],['ZmluZCA']
        ]


class SpecialWordChar_1(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_len = int(self.arg_list[0])
        self.preprocessing_type = str(self.arg_list[1])
        self.num_feat = self.max_len

        SWtoken_Arr = [
        [ # Basic
            ['alert', 'a', 0], ['alter', 'b', 0], ['and', 'c', 0], ['between', 'd', 0], ['cmd', 'e', 0],
            ['commit', 'f', 0], ['count', 'g', 0], ['exec', 'h', 0], ['from', 'i', 0], ['href', 'j', 0],
            ['insert', 'k', 0], ['into', 'l', 0], ['objectclass', 'm', 0], ['onmouseover', 'n', 0],
            ['script', 'o', 0], ['select', 'p', 0], ['shell', 'q', 0], ['table', 'r', 0], ['union', 's', 0],
            ['upper', 't', 0], ['or', 'u', 0], ['order', 'v', 0], ['passwd', 'w', 0], ['password', 'x', 0],
            ['where', 'y', 0], ['winnt', 'z', 0], ['onload', 'A', 0], ['cookie', 'B', 0], ['phpmyadmin', 'C', 0],
            ['wget', 'D', 0], ['curl', 'E', 0],
            #######################
            ['accept :', 'F', 0], ['0 %', 'G', 0], ['% 0a', 'H', 0], ['/ c', 'I', 0], ['cn =', 'J', 0],
            ['= - craw', 'K', 0], ['document . cookie', 'L', 0], ['etc / passwd', 'M', 0], ['# include', 'N', 0],
            ['javascript :', 'O', 0], ['mail =', 'P', 0], ['path / child', 'Q', 0], ['url =', 'R', 0],
            ['user - agent', 'S', 0], ['content - type', 'T', 0], ['information - schema', 'U', 0],
            ['bash _ history', 'V', 0],
        ],
        [  # FD
            ['etc', 'A', 0], ['opt', 'A', 0], ['proc', 'A', 0], ['root', 'A', 0], ['usr', 'A', 0],
            ['var', 'B', 0], ['inetpub', 'B', 0], ['recycle', 'B', 0], ['apache', 'B', 0], ['documents', 'B', 0],
            ['and', 'C', 0], ['settings', 'C', 0], ['home', 'C', 0], ['log', 'C', 0], ['logs', 'C', 0],
            ['minint', 'D', 0], ['mysql', 'D', 0], ['nginx', 'D', 0], ['php', 'D', 0], ['program', 'D', 0],
            ['files', 'E', 0], ['programfiles', 'E', 0], ['sysprep', 'E', 0], ['system', 'E', 0],
            ['volume', 'E', 0],
            ['information', 'F', 0], ['users', 'F', 0], ['wamp', 'F', 0], ['windows', 'F', 0], ['winnt', 'F', 0],
            ['xampp', 'G', 0], ['web', 'G', 0], ['inf', 'G', 0], ['config', 'G', 0], ['include', 'G', 0],
            ['inc', 'H', 0], ['sites', 'H', 0], ['phpmyadmin', 'H', 0], ['jeus', 'H', 0], ['library', 'H', 0],
            ['private', 'I', 0], ['httpd', 'I', 0], ['init', 'I', 0], ['lampp', 'I', 0], ['lamp', 'I', 0],
            ['self', 'J', 0], ['ssh', 'J', 0], ['local', 'J', 0], ['sysconfig', 'J', 0], ['administrator', 'J', 0],
            ['bin', 'K', 0], ['wwwroot', 'K', 0], ['smsosd', 'K', 0], ['data', 'K', 0], ['conf', 'K', 0],
            ['apache', 'L', 0], ['group', 'L', 0], ['apachegroup', 'L', 0], ['apache', 'L', 0],
            ['software', 'L', 0],
            ['foundation', 'M', 0], ['filezilla', 'M', 0], ['server', 'M', 0], ['inetsrv', 'M', 0],
            ['debug', 'M', 0],
            ['panther', 'N', 0], ['repair', 'N', 0], ['filezillaftp', 'N', 0], ['mercurymail', 'N', 0],
            ['sendmail', 'O', 0], ['tomcat', 'O', 0], ['webalizer', 'O', 0], ['webdav', 'O', 0],
            ['plugins', 'O', 0],
            ['defaults', 'P', 0], ['webserver', 'P', 0], ['sites', 'P', 0], ['available', 'P', 0],
            ['desktop', 'P', 0],
            ['stable', 'Q', 0], ['osdlogs', 'Q', 0], ['mysql', 'Q', 0], ['unattend', 'Q', 0], ['drivers', 'Q', 0],
            ['documents', 'R', 0], ['htdocs', 'R', 0], ['regback', 'R', 0], ['httperr', 'R', 0], ['extra', 'R', 0],
            ['schema', 'S', 0], ['passwd', 'S', 0],
            ###########################
            ['vhosts', 'T', 0], ['grub', 'T', 0], ['mkuser', 'T', 0], ['config', 'T', 0], ['passwd', 'T', 0],
            ['group', 'U', 0], ['hosts', 'U', 0], ['motd', 'U', 0], ['issue', 'U', 0], ['bashrc', 'U', 0],
            ['nginx', 'V', 0], ['boot', 'V', 0], ['version', 'V', 0], ['cmdline', 'V', 0], ['mounts', 'V', 0],
            ['host', 'W', 0], ['fstab', 'W', 0], ['sysprep', 'W', 0], ['unattended', 'W', 0], ['unattend', 'W', 0],
            ['shadow', 'X', 0], ['profile', 'X', 0], ['interrupts', 'X', 0], ['cpuinfo', 'X', 0],
            ['meminfo', 'X', 0],
            ['services', 'Y', 0], ['security', 'Y', 0], ['shells', 'Y', 0], ['resolv', 'Y', 0], ['fastab', 'Y', 0],
            ['login', 'Z', 0], ['ftproot', 'Z', 0], ['access', 'Z', 0], ['error', 'Z', 0], ['apache', 'Z', 0],
            ['systeminit', 'a', 0], ['robots', 'a', 0], ['humans', 'a', 0], ['style', 'a', 0],
            ['configuration', 'a', 0],
            ['wp', 'b', 0], ['login', 'b', 0], ['wp', 'b', 0], ['admin', 'b', 0], ['wp', 'b', 0],
            ['content', 'b', 0],
            ['my', 'c', 0], ['php', 'c', 0], ['sessions', 'c', 0], ['server', 'c', 0], ['local', 'c', 0],
            ['wpsettings', 'd', 0], ['explorer', 'd', 0], ['iis', 'd', 0], ['notepad', 'd', 0], ['system', 'd', 0],
            ['temp', 'e', 0], ['windowsupdate', 'e', 0], ['win', 'e', 0], ['weblogic', 'e', 0], ['mysql', 'e', 0],
            ['changelog', 'f', 0], ['properties', 'f', 0], ['mercury', 'f', 0], ['phpinfo', 'f', 0],
            ['sendmail', 'g', 0], ['webalizer', 'g', 0], ['webdav', 'g', 0], ['settings', 'g', 0],
            ['httpd', 'g', 0],
            ['sam', 'h', 0], ['software', 'h', 0], ['eula', 'h', 0], ['license', 'h', 0],
            ['sysprepsysprep', 'h', 0],
            ['sysprepunattended', 'i', 0], ['sysprepunattend', 'i', 0], ['index', 'i', 0], ['apachectl', 'i', 0],
            ['hostname', 'j', 0], ['mysql', 'j', 0], ['bin', 'j', 0], ['default', 'j', 0],
            ['applicationhost', 'j', 0],
            ['httperr', 'k', 0], ['aspnet', 'k', 0], ['schema', 'k', 0], ['ports', 'k', 0], ['httpd', 'k', 0],
            ['ssl', 'l', 0], ['desktop', 'l', 0], ['variables', 'l', 0], ['setupinfo', 'l', 0],
            ['appevent', 'l', 0],
            ['secevent', 'm', 0], ['tomcat', 'm', 0], ['users', 'm', 0], ['web', 'm', 0], ['appstore', 'm', 0],
            ['metabase', 'n', 0], ['netsetup', 'n', 0], ['conf', 'n', 0], ['environ', 'n', 0],
            ['authorized', 'n', 0],
            ['keys', 'o', 0], ['id', 'o', 0], ['rsa', 'o', 0], ['known', 'o', 0], ['hosts', 'o', 0],
            ['network', 'p', 0], ['ntuser', 'p', 0], ['logfiles', 'p', 0], ['global', 'p', 0], ['history', 'p', 0],
            ['htpasswd', 'q', 0], ['bash', 'q', 0], ['history', 'q', 0], ['my', 'q', 0],
            ##############################
            ['d', 'r', 0], ['conf', 'r', 0], ['default', 'r', 0], ['wsconfig', 'r', 0], ['ini', 'r', 0],
            ['gz', 'r', 0],
            ['bashrc', 's', 0], ['inf', 's', 0], ['txt', 's', 0], ['xml', 's', 0], ['defs', 's', 0],
            ['log', 's', 0],
            ['dat', 't', 0], ['css', 't', 0], ['php', 't', 0], ['cnf', 't', 0], ['exe', 't', 0], ['inc', 't', 0],
            ['rtf', 'u', 0], ['html', 'u', 0], ['err', 'u', 0], ['confetc', 'u', 0], ['config', 'u', 0],
            ['bak', 'v', 0], ['evt', 'v', 0], ['sav', 'v', 0], ['sa', 'v', 0], ['keystore', 'v', 0],
            ['pub', 'v', 0],
            ['asa', 'w', 0], ['asp', 'w', 0]
        ],
        [  # FUP
            ['zorback', 'A', 0], ['h4x0r', 'A', 0], ['awen', 'A', 0], ['perlkit', 'A', 0], ['darkraver', 'A', 0],
            ['carbylamine', 'B', 0], ['c99madshell', 'B', 0], ['azrail', 'B', 0], ['aspyqanalyser', 'B', 0],
            ['aspxspy', 'C', 0], ['asmodeus', 'C', 0], ['antichat', 'C', 0], ['aventgrup', 'C', 0],
            ['ru24postwebshell', 'D', 0], ['jspspy', 'D', 0], ['h4ntu', 'D', 0], ['entrika', 'D', 0],
            ['xiangxilianjie', 'E', 0], ['sqlrootkit', 'E', 0], ['kingdefacer', 'E', 0], ['lotfree', 'E', 0],
            ['backdoor', 'F', 0], ['bythehacker', 'F', 0], ['c99shell', 'F', 0], ['knull', 'F', 0],
            ['hackart', 'F', 0],
            ['ru24postwebshell', 'G', 0], ['phpwebshell', 'G', 0], ['rootshell', 'G', 0], ['nullshell', 'G', 0],
            ['aspshell', 'H', 0], ['myshell', 'H', 0], ['wshshell', 'H', 0], ['kcwebtelnet', 'H', 0],
            ['r57shell', 'I', 0], ['jspwebshell', 'I', 0],
            ##################
            ['shell', 'J', 0], ['exec', 'J', 0], ['passthru', 'J', 0], ['system', 'J', 0], ['popen', 'J', 0],
            ['eval', 'K', 0], ['command', 'K', 0], ['base64', 'K', 0], ['getparameter', 'K', 0], ['echo', 'K', 0],
            ['execl', 'L', 0], ['bin', 'L', 0], ['sh', 'L', 0], ['gzinflate', 'L', 0], ['decode', 'L', 0],
            ['uname', 'M', 0], ['execute', 'M', 0], ['createtextfile', 'M', 0], ['createobject', 'M', 0],
            ['phpremoteview', 'N', 0], ['fileoutputstream', 'N', 0], ['executecommand', 'N', 0],
            ['htmlencode', 'N', 0],
            ['getruntime', 'O', 0], ['runtime', 'O', 0], ['unzip', 'O', 0], ['mkdirs', 'O', 0],
            ['fileinputstream', 'P', 0], ['getabsolutepath', 'P', 0], ['replace', 'P', 0], ['function', 'P', 0],
            ['method', 'Q', 0], ['preg', 'Q', 0], ['str', 'Q', 0], ['base64decoder', 'Q', 0],
            ['decodebuffer', 'Q', 0],
            ['language', 'R', 0], ['filename', 'R', 0], ['filepath', 'R', 0], ['file', 'R', 0], ['name', 'R', 0],
            ['encode', 'S', 0], ['realpath', 'S', 0], ['formbase64string', 'S', 0], ['filesystemobject', 'S', 0],
            ['phpinfo', 'T', 0], ['getenv', 'T', 0], ['processbuilder', 'T', 0], ['popupmanagefile', 'T', 0],
            ['rot', 'U', 0], ['action', 'U', 0], ['curl', 'U', 0],
            #####################
            ['php', 'V', 0], ['asp', 'V', 0], ['jsp', 'V', 0], ['asa', 'V', 0], ['cdx', 'V', 0], ['war', 'V', 0],
            ['aspx', 'W', 0], ['zip', 'W', 0], ['cgi', 'W', 0], ['png', 'W', 0], ['gif', 'W', 0], ['jpeg', 'W', 0],
            ['exe', 'W', 0],
            ######################
            ['get', 'X', 0], ['post', 'X', 0], ['http', 'X', 0], ['title', 'X', 0], ['vbscript', 'X', 0],
            ['upload', 'Y', 0], ['upfile', 'Y', 0], ['uploads', 'Y', 0], ['popupfile', 'Y', 0], ['run', 'Y', 0],
            ['request', 'Z', 0], ['response', 'Z', 0], ['content', 'Z', 0], ['form', 'Z', 0], ['data', 'Z', 0],
            ['type', 'a', 0], ['encoding', 'a', 0], ['bytes', 'a', 0], ['filemanager', 'a', 0],
            ['uploadimage', 'a', 0],
            ['fileuploader', 'a', 0]
        ],
        [  # RCE
            ['memberaccess', 'A', 0], ['getsession', 'A', 0], ['getservletcontext', 'A', 0],
            ['getrealpath', 'A', 0],
            ['xmldatasource', 'B', 0], ['objectname', 'B', 0], ['management', 'B', 0], ['io', 'B', 0],
            ['fileoutputstream', 'C', 0], ['bufferedwriter', 'C', 0], ['dispatcher', 'C', 0],
            ['httpservletresponse', 'D', 0], ['lang', 'D', 0], ['runtime', 'D', 0], ['getruntime', 'D', 0],
            ['savegangster', 'E', 0], ['zglzcgf0y2hlci5idhrwu2vydmxldfjlcxvlc3q', 'E', 0],
            ['amf2ys5syw5nllbyb2nlc3ncdwlszgvy', 'F', 0], ['amf2ys5pby5jbnb1dfn0cmvhbvjlywrlcg', 'F', 0],
            ['inputstreamreader', 'G', 0], ['amf2ys5pby5gawxlt3v0chv0u3ryzwft', 'G', 0],
            ['amf2ys5pby5cdwzmzxjlzfdyaxrlcg', 'H', 0], ['zglzcgf0y2hlci5idhrwu2vydmxldfjlc3bvbnnl', 'H', 0],
            ['processbuilder', 'I', 0], ['allowstaticmethodaccess', 'I', 0], ['servletactioncontext', 'I', 0],
            ['methodaccessor', 'J', 0], ['denymethodexecution', 'J', 0], ['redirectaction', 'J', 0],
            ['ognlcontext', 'K', 0], ['memberacess', 'K', 0], ['redirect', 'K', 0], ['action', 'K', 0],
            ['annotationinvocationhandler', 'L', 0], ['annotation', 'L', 0], ['reflect', 'L', 0], ['class', 'L', 0],
            ['classloader', 'M', 0], ['xwork', 'M', 0], ['ognlutil', 'M', 0], ['redirecterrorstream', 'M', 0],
            ['setmemberaccess', 'N', 0], ['getinstance', 'N', 0], ['actioncontext', 'N', 0],
            ['getexcludedpackagenames', 'O', 0], ['getexcludedclasses', 'O', 0], ['getinputstream', 'O', 0],
            ['getwriter', 'P', 0], ['workcontext', 'P', 0], ['xmldecoder', 'P', 0], ['println', 'P', 0],
            ['unmarshaller', 'Q', 0], ['allowpackageprotectedaccess', 'Q', 0], ['allowprotectedaccess', 'Q', 0],
            ['allowprivateaccess', 'R', 0], ['excludedpackagenamepatterns', 'R', 0], ['excludedclasses', 'R', 0],
            ['invokeuq', 'S', 0], ['getruntimeur', 'S', 0], ['getmethoduq', 'S', 0],
            ['constanttransformerxv', 'S', 0],
            ['invokertransformer', 'T', 0], ['imethodnamet', 'T', 0], ['annotationinvocationhandleru', 'T', 0],
            ['invocationhandler', 'U', 0], ['runtimexpsr', 'U', 0], ['objectxpvq', 'U', 0], ['invoker', 'U', 0],
            ['createobject', 'U', 0],
            ######################################
            ['netstat', 'V', 0], ['uname', 'V', 0], ['ipconfig', 'V', 0], ['cmd', 'V', 0], ['root', 'V', 0],
            ['exe', 'W', 0], ['awzjb25mawc', 'W', 0], ['bmv0c3rhdcat', 'W', 0], ['exec', 'W', 0], ['dir', 'W', 0],
            ['rm', 'X', 0], ['rf', 'X', 0], ['mkdir', 'X', 0], ['ls', 'X', 0], ['ifconfig', 'X', 0],
            ['chmglq', 'Y', 0], ['bhntb2qg', 'Y', 0], ['bmv0c3rhdca', 'Y', 0], ['zgyg', 'Y', 0],
            ['dgnwzhvtcca', 'Z', 0], ['cgvybca', 'Z', 0], ['d2dldca', 'Z', 0], ['ymfzaca', 'Z', 0],
            ['y2qg', 'Z', 0],
            ['dm1zdgf0ia', 'a', 0], ['bhnvzia', 'a', 0], ['zgly', 'a', 0], ['zwnobya', 'a', 0], ['bmmglq', 'a', 0],
            ['cgluzya', 'b', 0], ['c2h1dgrvd24g', 'b', 0], ['a2lsbca', 'b', 0], ['dw5hbwug', 'b', 0],
            ['chdk', 'b', 0],
            ['bwtkaxig', 'c', 0], ['cm0glq', 'c', 0], ['dmkg', 'c', 0], ['bxyg', 'c', 0], ['y2htb2qg', 'c', 0],
            ['dg91y2gg', 'd', 0], ['bhmg', 'd', 0], ['y2f0ia', 'd', 0], ['y2f0pg', 'd', 0], ['c3uglq', 'd', 0],
            ['d2hvyw1p', 'e', 0], ['dg9wic0', 'e', 0], ['zgf0zq', 'e', 0], ['cgfzc3dk', 'e', 0],
            ['c3r0esa', 'e', 0],
            ['cm1kaxig', 'f', 0], ['bg4g', 'f', 0], ['y3ag', 'f', 0], ['y2hvd24g', 'f', 0], ['y2hncnag', 'f', 0],
            ['dw1hc2sg', 'g', 0], ['bw9yzsa', 'g', 0], ['agvhzca', 'g', 0], ['dgfpbca', 'g', 0], ['d2mg', 'g', 0],
            ['y3v0ia', 'h', 0], ['c29ydca', 'h', 0], ['c3bsaxqg', 'h', 0], ['z3jlcca', 'h', 0], ['zmluzca', 'h', 0],
            ['wget', 'i', 0], ['powershell', 'i', 0], ['curl', 'i', 0], ['nslookup', 'i', 0],
            #####################
            ['exefile', 'j', 0], ['jexws4', 'j', 0], ['singlesaints', 'j', 0], ['gry', 'j', 0], ['struts2', 'j', 0],
            ['showcase', 'k', 0], ['apache', 'k', 0], ['sun', 'k', 0], ['ognl', 'k', 0], ['soapenv', 'k', 0],
            ['member', 'l', 0], ['access', 'l', 0], ['acunetix', 'l', 0], ['soap', 'l', 0], ['javax', 'l', 0],
            ['java', 'm', 0], ['envelope', 'm', 0], ['method', 'm', 0], ['command', 'm', 0], ['xmlsoap', 'm', 0],
            ['sr', 'n', 0], ['sh', 'n', 0], ['coordinatorporttype', 'n', 0], ['appscan', 'n', 0],
            ['spider', 'n', 0],
            ########################################
            ['propfind', 'o', 0], ['content', 'o', 0], ['length', 'o', 0], ['head', 'o', 0], ['post', 'o', 0],
            ['get', 'p', 0], ['type', 'p', 0], ['user', 'p', 0], ['agent', 'p', 0], ['accept', 'p', 0],
            ['cookie', 'q', 0], ['prohibited', 'q', 0]
        ],
        [  # SQL
            ['case', 'A', 0], ['by', 'A', 0], ['all', 'A', 0], ['char', 'A', 0], ['character', 'A', 0],
            ['chr', 'B', 0], ['column', 'B', 0], ['concat', 'B', 0], ['convert', 'B', 0], ['count', 'B', 0],
            ['create', 'C', 0], ['declare', 'C', 0], ['delete', 'C', 0], ['distinct', 'C', 0], ['drop', 'C', 0],
            ['from', 'D', 0], ['function', 'D', 0], ['group', 'D', 0], ['having', 'D', 0], ['if', 'D', 0],
            ['ifnull', 'E', 0], ['insert', 'E', 0], ['into', 'E', 0], ['like', 'E', 0], ['limit', 'E', 0],
            ['or', 'F', 0], ['and', 'F', 0], ['order', 'F', 0], ['select', 'F', 0], ['union', 'F', 0],
            ['update', 'G', 0], ['when', 'G', 0], ['where', 'G', 0], ['grant', 'G', 0],
            #######################
            ['address', 'H', 0], ['data', 'H', 0], ['database', 'H', 0], ['dba', 'H', 0], ['etc', 'H', 0],
            ['file', 'I', 0], ['filename', 'I', 0], ['id', 'I', 0], ['name', 'I', 0], ['passwd', 'I', 0],
            ['password', 'J', 0], ['pg', 'J', 0], ['pwd', 'J', 0], ['resource', 'J', 0], ['sys', 'J', 0],
            ['system', 'K', 0], ['table', 'K', 0], ['tablename', 'K', 0], ['tables', 'K', 0], ['uid', 'K', 0],
            ['user', 'L', 0], ['username', 'L', 0], ['users', 'L', 0], ['utl', 'L', 0], ['value', 'L', 0],
            ['values', 'M', 0], ['version', 'M', 0], ['schema', 'M', 0], ['information', 'M', 0],
            ['inaddr', 'M', 0],
            ['admin', 'M', 0],
            #############################
            ['cmd', 'N', 0], ['cmdshell', 'N', 0], ['echo', 'N', 0], ['exe', 'N', 0], ['exec', 'N', 0],
            ['shell', 'O', 0], ['master', 'O', 0], ['xp', 'O', 0], ['sp', 'O', 0], ['regdelete', 'O', 0],
            ['availablemedia', 'P', 0], ['terminate', 'P', 0], ['regwrite', 'P', 0],
            ['regremovemultistring', 'P', 0],
            ['regread', 'Q', 0], ['regenumvalues', 'Q', 0], ['regenumkeys', 'Q', 0], ['regenumbalues', 'Q', 0],
            ['regdeletevalue', 'R', 0], ['regdeletekey', 'R', 0], ['regaddmultistring', 'R', 0], ['ntsec', 'R', 0],
            ['makecab', 'S', 0], ['loginconfig', 'S', 0], ['enumdsn', 'S', 0], ['filelist', 'S', 0],
            ['execresultset', 'T', 0], ['dirtree', 'T', 0], ['cmdshell', 'T', 0], ['reg', 'T', 0],
            ['servicecontrol', 'U', 0], ['webserver', 'U', 0],
            ############################
            ['decode', 'V', 0], ['default', 'V', 0], ['delay', 'V', 0], ['document', 'V', 0], ['eval', 'V', 0],
            ['getmappingxpath', 'W', 0], ['hex', 'W', 0], ['is', 'W', 0], ['login', 'W', 0], ['match', 'W', 0],
            ['not', 'X', 0], ['null', 'X', 0], ['request', 'X', 0], ['sets', 'X', 0], ['to', 'X', 0],
            ['var', 'Y', 0], ['varchar', 'Y', 0], ['waitfor', 'Y', 0], ['desc', 'Y', 0], ['connect', 'Y', 0],
            ['as', 'Z', 0], ['int', 'Z', 0], ['log', 'Z', 0], ['cast', 'Z', 0], ['rand', 'Z', 0], ['sleep', 'Z', 0],
            ['substring', 'a', 0], ['replace', 'a', 0], ['benchmark', 'a', 0], ['md', 'a', 0],
            #######################
            ['content', 'b', 0], ['cookie', 'b', 0], ['dbms', 'b', 0], ['db', 'b', 0], ['dir', 'b', 0],
            ['get', 'c', 0], ['http', 'c', 0], ['mysql', 'c', 0], ['oracle', 'c', 0], ['post', 'c', 0],
            ['query', 'd', 0], ['referer', 'd', 0], ['sql', 'd', 0], ['sqlmap', 'd', 0]
        ],
        [  # UAA
            ['myadmin', 'A', 0], ['manager', 'A', 0], ['admin', 'A', 0], ['wp', 'A', 0], ['saedit', 'A', 0],
            ['config', 'B', 0], ['funcspecs', 'B', 0], ['scripts', 'B', 0], ['server', 'B', 0], ['center', 'B', 0],
            ['tomcat', 'C', 0], ['pma', 'C', 0], ['transfer', 'C', 0], ['console', 'C', 0], ['vti', 'C', 0],
            ['acensus', 'D', 0], ['openapi', 'D', 0], ['jmx', 'D', 0], ['web', 'D', 0], ['conf', 'D', 0],
            ['servlet', 'E', 0], ['export', 'E', 0], ['cs', 'E', 0], ['db', 'E', 0], ['changelog', 'E', 0],
            ['status', 'F', 0], ['login', 'F', 0], ['setup', 'F', 0], ['info', 'F', 0], ['join', 'F', 0],
            ['encoding', 'G', 0], ['bin', 'G', 0], ['security', 'G', 0], ['empappupdtlogin', 'G', 0],
            ['content', 'H', 0], ['spmgr', 'H', 0], ['sap', 'H', 0], ['rd', 'H', 0], ['log', 'H', 0],
            ['details', 'I', 0], ['howto', 'I', 0], ['inc', 'I', 0], ['index', 'I', 0], ['check', 'I', 0],
            ['loginform', 'J', 0], ['service', 'J', 0], ['user', 'J', 0], ['plugins', 'J', 0],
            ['properties', 'J', 0],
            ['wsomg', 'K', 0], ['portal', 'K', 0], ['import', 'K', 0], ['gpin', 'K', 0], ['aut', 'K', 0],
            ['rest', 'L', 0], ['dzs', 'L', 0], ['csql', 'L', 0], ['dll', 'L', 0], ['edit', 'L', 0],
            ['view', 'L', 0],
            ['upload', 'M', 0], ['author', 'M', 0], ['resource', 'M', 0], ['zoomsounds', 'M', 0],
            ['phpmyadmin', 'N', 0], ['phpmyadminold', 'N', 0], ['bak', 'N', 0], ['pmapass', 'N', 0],
            ['pmahomme', 'O', 0], ['editor', 'O', 0], ['phpadmin', 'O', 0], ['configuration', 'O', 0],
            ['fckeditor', 'P', 0], ['inf', 'P', 0], ['phpmy', 'P', 0], ['ckfinder', 'P', 0],
            #######################################
            ['rhksflwk', 'Q', 0], ['master', 'Q', 0], ['admin', 'Q', 0], ['manager', 'Q', 0], ['webmaster', 'Q', 0],
            ['root', 'R', 0], ['administrator', 'R', 0], ['administrators', 'R', 0], ['superuser', 'R', 0],
            ['weblogic', 'S', 0], ['guest', 'S', 0], ['test', 'S', 0], ['ftpuser', 'S', 0], ['system', 'S', 0],
            ['scott', 'T', 0], ['tomcat', 'T', 0], ['user', 'T', 0], ['operator', 'T', 0], ['anonymous', 'T', 0],
            ['super', 'U', 0], ['pmauser', 'U', 0], ['mysqladmin', 'U', 0], ['sysmaster', 'U', 0],
            ['dbadmin', 'U', 0],
            ['pmaauth', 'V', 0], ['admindb', 'V', 0], ['administrateur', 'V', 0], ['administrat', 'V', 0],
            ['webmail', 'W', 0], ['adminmaster', 'W', 0], ['phpadmin', 'W', 0], ['testuser', 'W', 0],
            ['rootadmin', 'X', 0], ['adminid', 'X', 0],
            #######################################
            ['root', 'Y', 0], ['administrator', 'Y', 0], ['administrators', 'Y', 0], ['superuser', 'Y', 0],
            ['weblogic', 'Z', 0], ['asdf', 'Z', 0], ['qwer', 'Z', 0], ['test', 'Z', 0], ['passwd', 'Z', 0],
            ['qwerty', 'a', 0], ['password', 'a', 0], ['manager', 'a', 0], ['pass', 'a', 0], ['admin', 'a', 0],
            ['abcd', 'b', 0], ['aaaa', 'b', 0], ['asdfgh', 'b', 0], ['webmaster', 'b', 0], ['webmaste', 'b', 0],
            ['iisadminpwd', 'c', 0], ['asdfg', 'c', 0], ['rootroot', 'c', 0], ['rootpassword', 'c', 0],
            ['asdfasdf', 'd', 0], ['abcdefg', 'd', 0],
            ##########################################
            ['authorization', 'e', 0], ['basic', 'e', 0], ['zmeu', 'e', 0], ['python', 'e', 0], ['cpython', 'e', 0],
            ['scan', 'f', 0], ['testcookie', 'f', 0], ['ehlo', 'f', 0], ['baiduspider', 'f', 0]
        ],
        [  # XSS
            ['innerhtml', 'A', 0], ['script', 'A', 0], ['svg', 'A', 0], ['contenteditable', 'A', 0], ['x', 'A', 0],
            ['src', 'B', 0], ['iframe', 'B', 0], ['javascript', 'B', 0], ['embed', 'B', 0], ['math', 'B', 0],
            ['brute', 'C', 0], ['href', 'C', 0], ['form', 'C', 0], ['action', 'C', 0], ['input', 'C', 0],
            ['type', 'D', 0], ['submit', 'D', 0], ['isindex', 'D', 0], ['value', 'D', 0], ['button', 'D', 0],
            ['formaction', 'E', 0], ['srcdoc', 'E', 0], ['xlink', 'E', 0], ['img', 'E', 0], ['xmlns', 'E', 0],
            ['link', 'F', 0], ['base', 'F', 0], ['style', 'F', 0], ['marquee', 'F', 0], ['audio', 'F', 0],
            ['video', 'G', 0], ['keygen', 'G', 0], ['autofocus', 'G', 0], ['select', 'G', 0], ['option', 'G', 0],
            ['menu', 'H', 0], ['contextmenu', 'H', 0], ['textarea', 'H', 0], ['source', 'H', 0], ['meta', 'H', 0],
            ['object', 'I', 0], ['html', 'I', 0], ['target', 'I', 0], ['card ', 'I', 0], ['onevent', 'I', 0],
            ['animate', 'J', 0], ['handler', 'J', 0], ['feimage', 'J', 0], ['table', 'J', 0],
            ['background', 'J', 0],
            ['frameset', 'K', 0], ['div', 'K', 0], ['allowscriptaccess', 'K', 0],
            ###############################
            ['onload', 'L', 0], ['onmouseover', 'L', 0], ['onsubmit', 'L', 0], ['onfocus', 'L', 0],
            ['onblur', 'L', 0],
            ['onclick', 'M', 0], ['oncopy', 'M', 0], ['oncontextmenu', 'M', 0], ['oncut', 'M', 0],
            ['ondblclick', 'N', 0], ['ondrag', 'N', 0], ['oninput', 'N', 0], ['onkeydown', 'N', 0],
            ['onkeypress', 'O', 0], ['onkeyup', 'O', 0], ['onmousedown', 'O', 0], ['onmousemove', 'O', 0],
            ['onmouseout', 'P', 0], ['onmouseup', 'P', 0], ['onpaste', 'P', 0], ['ontouchstart', 'P', 0],
            ['ontouchend', 'R', 0], ['ontouchmove', 'R', 0], ['ontouchcancel', 'R', 0],
            ['onorientationchange', 'R', 0],
            ['onerror', 'S', 0], ['onpageshow', 'S', 0], ['onhashchange', 'S', 0], ['onscroll', 'S', 0],
            ['onresize', 'T', 0], ['onhelp', 'T', 0], ['onstart', 'T', 0], ['onloadstart', 'T', 0],
            ['onchange', 'U', 0], ['onshow', 'U', 0], ['oneonerrorrror', 'U', 0], ['ontoggle', 'U', 0],
            ['onafterscriptexecute', 'V', 0], ['onbeforescriptexecute', 'V', 0], ['onfinish', 'V', 0],
            ['expression', 'W', 0], ['onbeforeload', 'W', 0], ['onbeforeunload', 'W', 0], ['onformchange', 'W', 0],
            ['vbscript', 'W', 0],
            ##########################
            ['eval', 'X', 0], ['find', 'X', 0], ['top', 'X', 0], ['source', 'X', 0], ['tostring', 'X', 0],
            ['url', 'Y', 0], ['slice', 'Y', 0], ['location', 'Y', 0], ['hash', 'Y', 0], ['setInterval', 'Y', 0],
            ['function', 'Z', 0], ['appendchild', 'Z', 0], ['createelement', 'Z', 0], ['rel', 'Z', 0],
            ['string', 'a', 0], ['fromcharcode', 'a', 0], ['window', 'a', 0], ['parent', 'a', 0], ['self', 'a', 0],
            ['prompt', 'b', 0], ['defineproperties', 'b', 0], ['event', 'b', 0], ['initmouseevent', 'b', 0],
            ['childnodes', 'c', 0], ['clonenode', 'c', 0], ['match', 'c', 0], ['head', 'c', 0], ['substr', 'c', 0],
            ['unescape', 'd', 0], ['xmlhttp', 'd', 0], ['open', 'd', 0], ['content', 'd', 0], ['frames', 'd', 0],
            ['import', 'e', 0], ['behavior', 'e', 0], ['geturl', 'e', 0], ['charset', 'e', 0],
            #######################
            ['alert', 'f', 0], ['navigator', 'f', 0], ['vibrate', 'f', 0], ['document', 'f', 0], ['domain', 'f', 0],
            ['message', 'g', 0], ['write', 'g', 0], ['cookie', 'g', 0], ['echo', 'g', 0], ['exec', 'g', 0],
            ['cmd', 'h', 0], ['msgbox', 'h', 0],
            ########################
            ['xss', 'i', 0], ['hello', 'i', 0], ['fuzzelement', 'i', 0], ['test', 'i', 0], ['injectx', 'i', 0],
            ['netsparker', 'j', 0], ['openbugbounty', 'j', 0], ['baiduspider', 'j', 0], ['csrf', 'j', 0]
        ]]
        index_arr = ['Basic', 'FD', 'FUP', 'RCE', 'SQL', 'UAA', 'XSS']
        try :
            index = index_arr.index(self.preprocessing_type)
        except:
            index = 0 # Basic
        self.SWtoken = SWtoken_Arr[index]

        for i in range(len(self.SWtoken)):
            iLenTemp = len(self.SWtoken[i][0])
            self.SWtoken[i][2] = iLenTemp

        self.sorted_sw_token = sorted(self.SWtoken, key=itemgetter(2), reverse=True)

    def apply(self, data):
        try:
            data = data.replace("\\/", "/")
            if self.preprocessing_type == 'RCE':
                for rce in SWupper_arr:
                    if rce[0] != " ":
                        data = data.replace(str(rce[0]), ' ' + str(rce[0]) + ' ').replace("  ", " ")

            ####################################kps################################################
            data = data.replace("\r\n", " ").replace("\n", " ").replace("\t", " ").replace("  ", " ").replace("  ", " ")
            ####################################kps################################################
            ## URL Decode
            _input = data
            _input = _input.replace("CCOMMAA", ",")
            ####################################kps################################################
            # _input = _input.replace(",", "CCOMMAA")
            ####################################kps################################################
            try:
                iLoopCnt = 0
                val = ""
                while val != _input or iLoopCnt<=5:
                    val = _input
                    iLoopCnt += 1
                    _input = decode.unquote(_input.upper())
                dec_data = _input.lower()
            except:
                dec_data = str(_input).lower()

                dec_data = dec_data.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
            try:
                dec_data = re.findall(r'(?i)(get.*|post.*)', dec_data)[0]
                # self.LOGGER.getLogger().info(dec_data)
            except Exception as e:
                dec_data = dec_data
                # self.LOGGER.debug(e)
####################################kps################################################
            # IpFind = list(set(re.findall(r'[\W_]',dec_data)))
            #
            # for ix in range(10):
            #     IpFind.append(ix)
####################################kps################################################
####################################kps################################################
            IpFind = list(set(re.findall(r'[\W_0-9]', dec_data)))
####################################kps################################################
            for token in IpFind:
                if token != " ":
                    dec_data = dec_data.replace(str(token), ' '+str(token)+ ' ').replace("  ", " ")

            payload = dec_data
            payload = " " + payload + " "
            payload = payload.strip()
            IpCompare = []

            for word, change, len_word in self.sorted_sw_token :
                payload = payload.replace(" "+word+" "," ksshin"+change+" ")
                IpCompare.append("ksshin"+change)

####################################kps################################################
            # strTemp =""
            # resultPayload = payload.split(" ")
            #
            # for ChangeWord in resultPayload:
            #     if ChangeWord in IpFind or ChangeWord in IpCompare and ChangeWord != " ":
            #         strTemp = strTemp+ " " + ChangeWord.replace("ksshin", "")
            #
            # print(strTemp)
            # result = list()
            #
            # for i, ch in enumerate(strTemp):
            #     if ch != " ":
            #         result.append(ord(ch))
####################################kps################################################
####################################kps################################################
            resultPayload = payload.split(" ")
            result = list()

            for ChangeWord in resultPayload:
                try:
                    if (ChangeWord in IpFind or ChangeWord in IpCompare) and ChangeWord != " " and not ChangeWord.isdigit():
                        result.append(float(ord(ChangeWord.replace("ksshin", ""))))
                except Exception as e:
                    pass

####################################kps################################################
            ## padding
            # iMax = self.max_len - 4
            iMax = self.max_len
            padding0 = []
            bufferLen = len(result)
            if bufferLen < iMax:
                # padding0.extend([0.] * 2)
                padding0.extend(result)
                padding1 = [255.] * (iMax - bufferLen)
                padding0.extend(padding1)
                # padding0.extend([0.] * 2)
            elif bufferLen == iMax:
                # padding0.extend([0.] * 2)
                padding0.extend(result)
                # padding0.extend([0.] * 2)

            elif bufferLen > iMax:
                # padding0.extend([0.] * 2)
                padding0.extend(result[:iMax])
                # padding0.extend([0.] * 2)

            result = padding0

            return result


            # if result_len < self.max_len :
            #     padding = [255]*(self.max_len - result_len)
            #     result.extend(padding)
            #     return result
            # else :
            #     return result[:self.max_len]

        except Exception as e :
            self.LOGGER.debug(e, exc_info=True)
            return [255.] * self.max_len

    def get_num_feat(self):
        return self.max_len

if __name__ == '__main__':
    #data = "hjg yjhg 6ug679t g6guy g321%!#% $^$Fgsdfha"
    # data = "adsfafeafeGET /postal/mobile/popup/comm_newzipcd_mobileweb.jsp? classloader form_nameZGlzcGF0Y2hlci5IdHRwU2VydmxldFJlcXVlc3Q=sendForm&zip_name=tReceiverZipcode1&areacd_name=%7Ccat%20%2Fetc%2Fservices&addr1_name=tReceiverAddr1&addr2_name=tReceiverAddr2&addr3_name= HTTP/1.0 Accept-Language: ko Host: m.epost.go.kr Cookie: PCID=15236078361977256000040; serviceGbn=null; JSESSIONID=FF6slK0TNgixI03d9pS1Wvsxl8VA8hqcXDVo0Irc4G3z3fILMbpraEYRVhpRhfN5.epost3_servlet_parcel; mdt=ios; PHAROS_VISITOR=000000000162c2d79b0e529c0ade2518; cookieSequence=01382387; postname=%40%40%40%40%40%40abc%40%40%40%40%40%40abc%40%40%40%40%40%40abc; myquery=SCANW3B%0D%0ASPLITTING%2F%EB%93%B1%EA%B8%B0%EC%A1%B0%ED%9A%8C%2F%EB%82%B4%EC%9A%A9%EC%A6%9D%EB%AA%85%2F%EC%9A%B0%ED%8E%B8%EB%B2%88%ED%98%B8%EA%B2%80%EC%83%89%2F%EC%95%8C%EB%9C%B0%ED%8F%B0%2F%EB%8C%80%EC%B2%9C%EA%B9%80%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EB%8C%80%EC%B2%9C%EA%B9%80%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%95%8C%EB%9C%B0%ED%8F%B0%2F%EB%8C%80%EC%B2%9C%EA%B9%80%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%|"
    data = "/news/section/newsview.php?idxno=882273%25%27/**/aND/**/%278%27%3D%278"
    cvt_fn = SpecialWordChar_1(stat_dict=None, arg_list=[30, 'SQL']) # 스테이트딕이 민맥스가 있을경우 넣어줘야함, 아규리스트가 4인데 원소를 4개로 잘라서 몇개만 쓸껀지

    rst = cvt_fn.apply(data=data)
    print(rst)
    print(len(rst))
    # print(len(cvt_fn.apply(data="//")))
