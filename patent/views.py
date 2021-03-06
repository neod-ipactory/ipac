import os
import json, xmljson
import requests
import httplib2
import xmltodict

from django.db.models import Q, Count
from datetime import datetime, timedelta
from collections import OrderedDict, Counter
from django.http import JsonResponse
from django.views import View
from .models import Master, History
from .utils import query_debugger, tagsearch
from tag.models import Tag, Category
from my_settings import KIPRIS

class ChartView(View):
    @query_debugger
    def get(self, request):
        date_type = request.GET.get("date", None)
        f_date = request.GET.get("f_date", None)
        e_date = request.GET.get("e_date", None)
        try:
            if date_type == 'year':
                dates = [f_date, e_date]
                start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
                a = list(OrderedDict(((start + timedelta(_)).strftime(r"%Y"), None) for _ in range((end - start).days)).keys())
                chart1 = []
                chart2 = []
                for x in a:
                    base = [x, Master.objects.filter(file_date__contains = x).count()]
                    base2 =[x, Master.objects.filter(pub_date__contains = x).count()]
                    chart1.append(base)
                    chart2.append(base2)

                dm = Master.objects.filter(file_date__range=(start, end))
                mm = [j.major for j in dm]
                md = Counter(mm)
                sort_orders = sorted(md.items(), key=lambda x: x[1], reverse=True)
                pro = [(h.main_inventor, h.major) for h in dm]
                pros = Counter(pro)
                pro_orders = sorted(pros.items(), key=lambda x: x[1], reverse=True)
                coworks = []
                for t in dm:
                    t1 = t.applicant.split(' | ')
                    coworks = coworks + t1
                
                cowork = Counter(coworks)
                co_orders = sorted(cowork.items(), key=lambda x: x[1], reverse=True)

                return JsonResponse({
                    "chart1":chart1,
                    "chart2":chart2,
                    "major" :sort_orders,
                    "professor":pro_orders,
                    "cowork": co_orders
                })
        
            elif date_type == 'month':
    # 기간에 대해 정리
                dates = [f_date, e_date]
                start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
                a = list(OrderedDict(((start + timedelta(_)).strftime("%Y-%m"), None) for _ in range((end - start).days)).keys())
    # 조건별로 호출
                chart1 = []
                chart2 = []
                for x in a:
                    base = [x, Master.objects.filter(file_date__contains = x).count()]
                    base2 =[x, Master.objects.filter(pub_date__contains = x).count()]
                    chart1.append(base)
                    chart2.append(base2)

                dm = Master.objects.filter(file_date__range=(start, end))
                mm = [j.major for j in dm]
                md = Counter(mm)
                sort_orders = sorted(md.items(), key=lambda x: x[1], reverse=True)
                pro = [h.main_inventor for h in dm]
                pros = Counter(pro)
                pro_orders = sorted(pros.items(), key=lambda x: x[1], reverse=True)
                coworks = []
                for t in dm:
                    t1 = t.applicant.split(' | ')
                    coworks = coworks + t1
                
                cowork = Counter(coworks)
                co_orders = sorted(cowork.items(), key=lambda x: x[1], reverse=True)

                return JsonResponse({
                    "chart1":chart1,
                    "chart2":chart2,
                    "major" :sort_orders,
                    "professor":pro_orders,
                    "cowork": co_orders
                })
            
            elif date_type == 'day':
    # 기간에 대해 정리
                dates = [f_date, e_date]
                start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
                a = list(OrderedDict(((start + timedelta(_)).strftime("%Y-%m-%d"), None) for _ in range((end - start).days)).keys())
    # 조건별로 호출
                chart1 = []
                chart2 = []
                for x in a:
                    base = [x, Master.objects.filter(file_date__contains = x).count()]
                    base2 =[x, Master.objects.filter(pub_date__contains = x).count()]
                    chart1.append(base)
                    chart2.append(base2)

                dm = Master.objects.filter(file_date__range=(start, end))
                mm = [j.major for j in dm]
                md = Counter(mm)
                sort_orders = sorted(md.items(), key=lambda x: x[1], reverse=True)
                pro = [h.main_inventor for h in dm]
                pros = Counter(pro)
                pro_orders = sorted(pros.items(), key=lambda x: x[1], reverse=True)
                coworks = []
                for t in dm:
                    t1 = t.applicant.split(' | ')
                    coworks = coworks + t1
                
                cowork = Counter(coworks)
                co_orders = sorted(cowork.items(), key=lambda x: x[1], reverse=True)

                return JsonResponse({
                    "chart1":chart1,
                    "chart2":chart2,
                    "major" :sort_orders,
                    "professor":pro_orders,
                    "cowork": co_orders
                })

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"})

    def post(self, request):
        data =json.loads(request.body)
        dates = [data['f_date'], data['e_date']]
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        uno = Master.objects.filter(Q(file_date__range=(start, end))&Q(major__contains=data['major']))
        dos = [i.main_inventor for i in uno]
        tres = Counter(dos)
        quatro = sorted(tres.items(), key=lambda x:x[1], reverse=True)

        return JsonResponse({f"Professor in {data['major']}":quatro})


class UpdateMaster(View):
    def get(self, request):
        base = Master.objects.all().order_by("-file_date")[:1]
        for x in base:
            file_num = "".join(x.file_num.split('-'))
            url = f'http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getBibliographyDetailInfoSearch?applicationNumber={file_num}&ServiceKey={KIPRIS}'
            h = httplib2.Http()
            response, content = h.request(url, 'GET')
            result = content.decode('utf-8')
            jsonString = json.dumps(xmltodict.parse(result), indent=4)
            json2 = json.loads(jsonString)
            path = json2['response']['body']['item']['biblioSummaryInfoArray']['biblioSummaryInfo']
            path2 = json2['response']['body']['item']["abstractInfoArray"]["abstractInfo"]
            path3 = json2['response']['body']['item']["claimInfoArray"]["claimInfo"]
            path4 = json2['response']['body']['item']["applicantInfoArray"]["applicantInfo"]
            path5 = json2['response']['body']['item']["inventorInfoArray"]["inventorInfo"]
            path6 = json2['response']['body']['item']["imagePathInfo"]
            print(path['applicationNumber'])
            x.title  = path["inventionTitle"]
            x.title2 = path["inventionTitleEng"]
            x.abstract = path2["astrtCont"]
            x.claim = path3[0]["claim"]
            x.file_num = path["applicationNumber"]
            x.file_date= path["applicationDate"].replace('.','-')
            x.pub_num = path["openNumber"]
            x.pub_date = path["openDate"].replace('.','-')
            x.pub_num2 = path["publicationNumber"]
            x.pub_date2 = path["publicationDate"]
            x.reg_num = path["registerNumber"]
            x.reg_date = path["registerDate"].replace('.','-') if path["registerDate"] != None else None 
            x.applicant = path4['name']
            x.applicant2 = path4["engName"]
            x.inventor = path5['name']
            x.status = path["registerStatus"]
            x.img_src = path6["largePath"]
            x.save()

            return JsonResponse({"message":"success"})

class MainView(View):
    @query_debugger
    def get(self, request):
        tags = Tag.objects.select_related('category').prefetch_related('tagmaster').all()
        tag_bucket = []
        for i in tags:
            a = (i.name, i.code, i.count)
            tag_bucket.append(a)
        
        category_bucket = []
        for x in Category.objects.all():
            category_bucket.append([x.name, x.count])

        base = Master.objects.all()
        major = [x.major for x in base]
        m = Counter(major)
        major_bucket = sorted(m.items(), key=lambda x:x[0])
        grade = [x.claim_grade for x in base]
        mm = Counter(grade)
        grade_bucket = sorted(mm.items(), key=lambda x:x[0])

        return JsonResponse({
            "category":category_bucket,
            "tags":tag_bucket,
            "major":major_bucket,
            "grade":grade_bucket
        })

    @query_debugger
    def post(self, request):
        data = json.loads(request.body)
        kk = data['tag'].split(',')
        ll = data['status'].split(',')
        uu = data['major'].split(',')
        gg = data['grade'].split(',')
        y  = data['condition']
        td = data['date'].split(',')
        index2 = tagsearch(y,kk,td)
        stu = '서울과학기술대학교 산학협력단'

        if data['condition'] =='and':
            if data['stu'] == 0:
                if data['tag'] in data.values() or data['status'] in data.values() or data['major'] or data['grade'] in data.values(): 

                    if data['status'] == "" and data['major'] =="" and data['grade']=="":
                        index1 = index2
                    elif data['major'] == "" and data['grade'] == "":
                        index1 = index2.filter(status_krjp__in=ll)
                    elif data['status'] =="" and data['grade'] == "":
                        index1 = index2.filter(major__in=uu)
                    elif data['major'] == "" and data['status'] == 0:
                        index1 = index2.filter(claim_grade__in=gg)
                    elif data['major'] == "":
                        index1 = index2.filter(Q(status_krjp__in=ll) & Q(claim_grade__in=gg))
                    elif data['status'] =="":
                        index1 = index2.filter(Q(major__in=uu) & Q(claim_grade__in=gg))
                    elif data['grade'] == "":
                        index1 = index2.filter(Q(major__in=uu) & Q(status_krjp=ll))
                    else:
                        index1 = index2.filter(Q(status_krjp__in=ll) & Q(major__in=uu) & Q(claim_grade__in=gg))

                    tag_set=[]
                    uni_set=[]
                    grade_set=[]
                    for i in index1:
                        l = i.tags.split('|')
                        tag_set = tag_set + l
                        uni_set.append(i.major)
                        grade_set.append(i.claim_grade)

                    c = Counter(tag_set)
                    dd = list(c.values())
                    tagbase = Tag.objects.select_related('category').all()
                    bucket = []
                    for x,y in zip(c, dd):
                        bucket.append([
                            tagbase.get(code=x).name, x, y])
                    
                    tag_orders = sorted(bucket, key=lambda x: x[1])
                    listShow = [x.file_num for x in index1]
                    major = Counter(uni_set)
                    major_bucket = sorted(major.items(), key=lambda x:x[0])
                    grade= Counter(grade_set)
                    grade_bucket = sorted(grade.items(), key=lambda x:x[0])

                    return JsonResponse({"totalNumber":index1.count(),"listshow":listShow,"totalTag":len(tag_set),"data":tag_orders,"major":major_bucket,"grade":grade_bucket})

                else:
                    return JsonResponse({"message":"KeyError"})

                    
            elif data['stu'] == 1:
                if data['tag'] in data.values() or data['status'] in data.values() or data['major'] in data.values() or data['grade'] in data.values(): 
                    
                    if data['status'] == "" and data['major'] =="" and data['grade']=="":
                        index1 = index2.filter(applicant__exact=stu)
                    elif data['major'] == "" and data['grade'] == "":
                        index1 = index2.filter(Q(status_krjp__in=ll) & Q(applicant__exact=stu))
                    elif data['status'] =="" and data['grade'] == "":
                        index1 = index2.filter(Q(major__in=uu) & Q(applicant__exact=stu))
                    elif data['major'] == "" and data['status'] == 0:
                        index1 = index2.filter(Q(claim_grade__in=gg) & Q(applicant__exact=stu))
                    elif data['major'] == "":
                        index1 = index2.filter(Q(status_krjp__in=ll) & Q(claim_grade__in=gg) & Q(applicant__excat=stu))
                    elif data['status'] =="":
                        index1 = index2.filter(Q(major__in=uu) & Q(claim_grade__in=gg) & Q(applicant__excat=stu))
                    elif data['grade'] == "":
                        index1 = index2.filter(Q(major__in=uu) and Q(status_krjp=ll) & Q(applicant__exact=stu))
                    else:
                        index1 = index2.filter(Q(status_krjp__in=ll) & Q(major__in=uu) & Q(claim_grade__in=gg) & Q(applicant__exact=stu))
                    
                    tag_set=[]
                    uni_set=[]
                    grade_set=[]
                    for i in index1:
                        l = i.tags.split('|')
                        tag_set = tag_set + l
                        uni_set.append(i.major)
                        grade_set.append(i.claim_grade)

                    c = Counter(tag_set)
                    dd = list(c.values())
                    tagbase = Tag.objects.select_related('category').all()
                    bucket = []
                    for x,y in zip(c, dd):
                        bucket.append([
                            tagbase.get(code=x).name, x, y])
                    
                    tag_orders = sorted(bucket, key=lambda x: x[1])
                    listShow = [x.file_num for x in index1]
                    major = Counter(uni_set)
                    major_bucket = sorted(major.items(), key=lambda x:x[0])
                    grade= Counter(grade_set)
                    grade_bucket = sorted(grade.items(), key=lambda x:x[0])

                    return JsonResponse({"totalNumber":index1.count(),"listshow":listShow,"totalTag":len(tag_set),"data":tag_orders,"major":major_bucket,"grade":grade_bucket})

                else:
                    return JsonResponse({"message":"KeyError"})
        
        elif data['condition'] == 'or':
            print("or")
            if data['stu'] == 0:
                if data['tag'] in data.values() or data['status'] in data.values() or data['major'] or data['grade']: 

                    if data['status'] == "" and data['major'] =="" and data['grade']=="":
                        index1 = tagsearch(y,kk,td)
                    elif data['major'] == "" and data['grade'] == "":
                        #index2 = tagsearch(y,kk)
                        index1 = index2.filter(status_krjp__in=ll)
                    elif data['status'] =="" and data['grade'] == "":
                        #index2 = tagsearch(y,kk)
                        index1 = index2.filter(major__in=uu)
                    elif data['major'] == "" and data['status'] == 0:
                        #index2 = tagsearch(y,kk)
                        index1 = index2.filter(claim_grade__in=gg)
                    elif data['major'] == "":
                        #index2 = tagsearch(y,kk)
                        index1 = index2.filter(Q(status_krjp__in=ll) | Q(claim_grade__in=gg))
                    elif data['status'] =="":
                        #index2 = tagsearch(y,kk)
                        index1 = index2.filter(Q(major__in=uu) | Q(claim_grade__in=gg))
                    elif data['grade'] == "":
                        #index2 = tagsearch(y,kk)
                        index1 = index2.filter(Q(major__in=uu) | Q(status_krjp=ll))
                    else:
                        #index2 = tagsearch(y,kk)
                        index1 = index2.filter(Q(status_krjp__in=ll) | Q(major__in=uu) | Q(claim_grade__in=gg))

                    tag_set=[]
                    uni_set=[]
                    grade_set=[]
                    for i in index1:
                        l = i.tags.split('|')
                        tag_set = tag_set + l
                        uni_set.append(i.major)
                        grade_set.append(i.claim_grade)

                    c = Counter(tag_set)
                    dd = list(c.values())
                    tagbase = Tag.objects.select_related('category').all()
                    bucket = []
                    for x,y in zip(c, dd):
                        bucket.append([
                            tagbase.get(code=x).name, x, y])
                    
                    tag_orders = sorted(bucket, key=lambda x: x[1])
                    listShow = [x.file_num for x in index1]
                    major = Counter(uni_set)
                    major_bucket = sorted(major.items(), key=lambda x:x[0])
                    grade= Counter(grade_set)
                    grade_bucket = sorted(grade.items(), key=lambda x:x[0])

                    return JsonResponse({"totalNumber":index1.count(),"listshow":listShow,"totalTag":len(tag_set),"data":tag_orders,"major":major_bucket,"grade":grade_bucket})

                else:
                    return JsonResponse({"message":"KeyError"})

                    
            elif data['stu'] == 1:
                if data['tag'] in data.values() or data['status'] in data.values() or data['major'] or data['grade']: 

                    if data['status'] == "" and data['major'] =="" and data['grade']=="":
                        index1 = index2.filter(applicant__exact=stu)
                    elif data['major'] == "" and data['grade'] == "":
                        index1 = index2.filter(Q(status_krjp__in=ll) & Q(applicant__exact=stu))
                    elif data['status'] =="" and data['grade'] == "":
                        index1 = index2.filter(Q(major__in=uu) & Q(applicant__exact=stu))
                    elif data['major'] == "" and data['status'] == 0:
                        index1 = index2.filter(Q(claim_grade__in=gg) & Q(applicant__exact=stu))
                    elif data['major'] == "":
                        index1 = index2.filter(Q(status_krjp__in=ll) or Q(claim_grade__in=gg) & Q(applicant__exact=stu))
                    elif data['status'] =="":
                        index1 = index2.filter(Q(major__in=uu) or Q(claim_grade__in=gg) & Q(applicant__exact=stu))
                    elif data['grade'] == "":
                        index1 = index2.filter(Q(major__in=uu) or Q(status_krjp=ll) & Q(applicant__exact=stu))
                    else:
                        index1 = index2.filter(Q(status_krjp__in=ll) or Q(major__in=uu) or Q(claim_grade__in=gg) & Q(applicant__exact=stu))
                    
                    tag_set=[]
                    uni_set=[]
                    grade_set=[]
                    for i in index1:
                        l = i.tags.split('|')
                        tag_set = tag_set + l
                        uni_set.append(i.major)
                        grade_set.append(i.claim_grade)

                    c = Counter(tag_set)
                    dd = list(c.values())
                    tagbase = Tag.objects.select_related('category').all()
                    bucket = []
                    for x,y in zip(c, dd):
                        bucket.append([
                            tagbase.get(code=x).name, x, y])
                    
                    tag_orders = sorted(bucket, key=lambda x: x[1])
                    listShow = [x.file_num for x in index1]
                    major = Counter(uni_set)
                    major_bucket = sorted(major.items(), key=lambda x:x[0])
                    grade= Counter(grade_set)
                    grade_bucket = sorted(grade.items(), key=lambda x:x[0])

                    return JsonResponse({"totalNumber":index1.count(),"listshow":listShow,"totalTag":len(tag_set),"data":tag_orders,"major":major_bucket,"grade":grade_bucket})

                else:
                    return JsonResponse({"message":"KeyError"})

class KeywordSearch(View):
    def post(self, request):
        data = json.loads(request.body)
        word = data['keyword']
        try:
            answer = Master.objects.filter(Q(title__icontains=word) | Q(abstract__icontains=word) | Q(claim__icontains=word) | Q(inventor__icontains=word) | Q(applicant__icontains=word) |Q(applicant__icontains=word))
            bucket = [x.file_num for x in answer]
            return JsonResponse({
                "number":len(bucket),
                "result":bucket})
        
        except KeyError:
            JsonResponse({"mesage":"KEY_ERROR"})

class ListView(View):
    @query_debugger
    def post(self, request):
        data=json.loads(request.body)
        list_bucket = []
        for x in data['listshow']:
            base = Master.objects.get(file_num=x)
            tagging = base.tags.split('|')
            tag_bucket = []
            for i in tagging:
                t = Tag.objects.get(code=i)
                tag_bucket.append([t.name,t.code])
            source = ({
                "status": base.status_krjp,
                "file_num, file_date":(base.file_num, base.file_date),
                "pub_num, pub_date":(base.pub_num, base.pub_date),
                "applicant, inventor":(base.applicant.split(' |'), base.inventor.split(' | ')),
                "patentee":base.patentee,
                "major, main_inventor":(base.major, base.main_inventor),
                "grade":base.claim_grade,
                "title, tags":(base.title, tag_bucket),
            })
            list_bucket.append(source)

        return JsonResponse({"list":list_bucket})

class DetailView(View):
    @query_debugger
    def post(self, request):
        data=json.loads(request.body)
        list_bucket = []
        for x in data['listshow']:
            base = Master.objects.get(file_num=x)
            tagging = base.tags.split('|')
            tag_bucket = []
            for i in tagging:
                t = Tag.objects.get(code=i)
                tag_bucket.append([t.name,t.code])
            source = ({
                "number":data['listshow'].index(x)+1,
                "title":base.title,
                "applicant, inventor":(base.applicant.split(' |'), base.inventor.split(' | ')),
                "major, main_inventor":(base.major, base.main_inventor),
                "patentee":base.patentee,
                "file_num, file_date":(base.file_num, base.file_date),
                "pub_num, pub_date":(base.pub_num, base.pub_date),
                "reg_num, reg_date":(base.reg_num, base.reg_date),
                "tag":tag_bucket,
                "abstract":base.abstract,
                "claim":base.claim,
                "main_image":"update soon"
            })
            list_bucket.append(source)

        return JsonResponse({
            "side":"",
            "list":list_bucket})

class Register(View):
    @query_debugger
    def post(self, request):
        '''
        base = request.FILES['pdf']
        parsed_data = pdftodocs(base)
        data = json.loads(parsed_data)
        Master.objects.create(
            title = data['title'],
        ).save()
        '''
        pass


class TestView(View):
    def get(self, request):
        apply_num = Master.objects.all().last()
        b = apply_num.file_num.split('-')
        n = ''
        for i in b:
            n = n + i
        
        url = f'http://plus.kipris.or.kr/openapi/rest/RelatedDocsonfilePatService/relatedDocsonfileInfo?applicationNumber={n}&accessKey=QWSwer5evYdATtLpvybUIqIPUQZR6ATVfDNMLksLZMU='


        h = httplib2.Http()
        response, content = h.request(url, 'GET')
        result = content.decode('utf-8')
        jsonString = json.dumps(xmltodict.parse(result), indent=4)
        json2 = json.loads(jsonString)
        ff = len(json2['response']['body']['items']['relateddocsonfileInfo'])
        t = json2['response']['body']['items']['relateddocsonfileInfo']
        for i in t:
            if History.objects.filter(documentNumber=i['documentNumber']).exists():
                pass
            else:
                History.objects.create(
                    applicationNumber = i['applicationNumber'],
                    documentNumber    = i['documentNumber'],
                    documentDate      = i['documentDate'],
                    documentTitle     = i['documentTitle'],
                    documentTitleEng  = i['documentTitleEng'],
                    status            = i['status'],
                    statusEng         = i['statusEng'],
                    step              = i['step'],
                    trialNumber       = i['trialNumber'],
                    registrationNumber = i['registrationNumber'],
                    master_id         = apply_num.data_id)
            
        return JsonResponse({"message":"success"})
