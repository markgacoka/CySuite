import re


class Parser:

    def __init__(self, results, word):
        self.results = results
        self.word = word
        self.temp = []

    def genericClean(self):
        self.results = self.results.replace('<em>', '').replace('<b>', '').replace('</b>', '').replace('</em>', '')\
            .replace('%2f', '').replace('%3a', '').replace('<strong>', '').replace('</strong>', '')\
            .replace('<wbr>', '').replace('</wbr>', '')

        for e in ('<', '>', ':', '=', ';', '&', '%3A', '%3D', '%3C', '/', '\\'):
            self.results = self.results.replace(e, ' ')

    def urlClean(self):
        self.results = self.results.replace('<em>', '').replace('</em>', '').replace('%2f', '').replace('%3a', '')
        for e in ('<', '>', ':', '=', ';', '&', '%3A', '%3D', '%3C'):
            self.results = self.results.replace(e, ' ')

    def emails(self):
        self.genericClean()
        # Local part is required, charset is flexible.
        # https://tools.ietf.org/html/rfc6531 (removed * and () as they provide FP mostly)
        reg_emails = re.compile(r'[a-zA-Z0-9.\-_+#~!$&\',;=:]+' + '@' + '[a-zA-Z0-9.-]*' + self.word.replace('www.', ''))
        self.temp = reg_emails.findall(self.results)
        emails = self.unique()
        true_emails = {str(email)[1:].lower().strip() if len(str(email)) > 1 and str(email)[0] == '.'
                       else len(str(email)) > 1 and str(email).lower().strip() for email in emails}
        # if email starts with dot shift email string and make sure all emails are lowercase
        return true_emails

    def fileurls(self, file):
        urls = []
        reg_urls = re.compile('<a href="(.*?)"')
        self.temp = reg_urls.findall(self.results)
        allurls = self.unique()
        for x in allurls:
            if x.count('webcache') or x.count('google.com') or x.count('search?hl'):
                pass
            else:
                urls.append(x)
        return urls

    def hostnames(self):
        self.genericClean()
        reg_hosts = re.compile(r'[a-zA-Z0-9.-]*\.' + self.word)
        self.temp = reg_hosts.findall(self.results)
        hostnames = self.unique()
        reg_hosts = re.compile(r'[a-zA-Z0-9.-]*\.' + self.word.replace('www.', ''))
        self.temp = reg_hosts.findall(self.results)
        hostnames.extend(self.unique())
        return list(set(hostnames))

    
    def hostnames_all(self):
        reg_hosts = re.compile('<cite>(.*?)</cite>')
        temp = reg_hosts.findall(self.results)
        for x in temp:
            if x.count(':'):
                res = x.split(':')[1].split('/')[2]
            else:
                res = x.split('/')[0]
            self.temp.append(res)
        hostnames = self.unique()
        return hostnames

    def set(self):
        reg_sets = re.compile(r'>[a-zA-Z0-9]*</a></font>')
        self.temp = reg_sets.findall(self.results)
        sets = []
        for x in self.temp:
            y = x.replace('>', '')
            y = y.replace('</a</font', '')
            sets.append(y)
        return sets

    def urls(self):
        found = re.finditer(r'(http|https)://(www\.)?trello.com/([a-zA-Z0-9\-_\.]+/?)*', self.results)
        urls = {match.group().strip() for match in found}
        return urls

    def unique(self) -> list:
        self.new = []
        for x in self.temp:
            if x not in self.new:
                self.new.append(x)
        return self.new
