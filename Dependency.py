#REQUIRES Stanford parser full. (Search google, download, and unzip)
#USAGE:
#      compare_pages(txt1,txt2)
#  txt1: string of sentences seperated by newline characters.
#  txt2: string of sentences sperated by new line characters
#
#RETURNS:
#   For every conflicting sentence (in the other document):
#CONFLICT!: 
#   marijuana is healthy.
#   marijuana is not healthy.

from nltk.parse.stanford import StanfordDependencyParser
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


path_to_jar = '/home/b/Documents/stanford-parser-full-2015-12-09/stanford-parser.jar'
path_to_models_jar = '/home/b/Documents/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)



def get_dep_for_sent(sent="Marijuna is not healthy"):
    result = dependency_parser.raw_parse(sent.lower())
    dep = result.next()
    return list(dep.triples())    

def look_for_dep_tag(lst, tag):
    nlst = []
    for trip in lst:
        if trip[1] == tag:
            verb = str(trip[0][0]).lower()
            noun = str(trip[-1][0]).lower()
            nlst.append((verb,tag,noun))
    return nlst

def doc_to_dict(doc):
    #doc_dict is in form {sent:dep}
    doc_dict = {}
    for line in doc.split("\n"):
        if len(line.strip()) == 0:
            continue
        doc_dict[line.strip().lower()] = get_dep_for_sent(line.lower().strip())
    return doc_dict

def conflict(sent1,sent2):
    dobjs1 = look_for_dep_tag(sent1,"dobj")
    dobjs2 = look_for_dep_tag(sent2,"dobj")
    check_neg = []
    
    for i in dobjs1:
        for j in dobjs2:
            if i==j:
                verb = i[0]
                
                dnsub1 = look_for_dep_tag(sent1,"nsubj")
                dnsub2 = look_for_dep_tag(sent2,"nsubj")
                
                for k in dnsub1:
                    for l in dnsub2:
                        if k[0] == verb:
                            if k == l:
                                check_neg.append(verb)
    
    for ii in check_neg:
        t1 = False
        t2 = False
        dneg1 = look_for_dep_tag(sent1,"neg")
        for r in dneg1:
            if r[0] == ii:
                t1 = True
        dneg2 = look_for_dep_tag(sent2,"neg")
        for r in dneg2:
            if r[0] == ii:
                t2 = True
        if (t1 and not t2) or (t2 and not t1):
            return True
    return False

def conflict2(sent1,sent2):
    neg1 = look_for_dep_tag(sent1,"neg")
    neg2 = look_for_dep_tag(sent2,"neg")    
    bools = None
    for i in neg1:
        if i not in neg2:
            #negated in 1 but not in 2
            bools = conflict2_sub(sent1,sent2, i)
            if bools:
                return True
    
    for i in neg2:
        if i not in neg1:
            #negated in 2 but not 1
            bools = conflict2_sub(sent2,sent1, i)
            if bools:
                return True
    return False

def conflict2_sub(sent1,sent2, neg):
    negated = neg[0]

    t1_trips = []
    t2_trips = []
    
    for i in sent1:
        if i[1] == "neg":
            continue
        a = i[0][0]
        b = i[-1][0]
        
        if a == negated or b == negated:
            t1_trips.append(i)
            
    for j in sent2:     
        a = j[0][0]
        b = j[-1][0]        
        if a == negated or b == negated:
            t2_trips.append(j)
    
    t1_trips.sort()
    t2_trips.sort()
    
    #DEBUG PRINTING
    #print t1_trips, sent1
    #print neg
    #print t2_trips, sent2
    
    if len(t1_trips) > len(t2_trips):
        #loop over t2
        counter = 0
        for i in t2_trips:
            if i in t1_trips:
                counter+=1
        percentage = float(counter)/len(t1_trips)
    else:
        #loop over t1
        counter = 0
        for i in t1_trips:
            if i in t2_trips:
                counter+=1
        percentage = float(counter)/len(t2_trips)
    
    if percentage > 0.5:
        return True
    return False
    
txt1 = '''
There is absolutely undeniable scientific proof that vaccines cause autism.
There is no question!
Case closed!
Game over!
The people and the mainstream media  who claim that the vaccine autism link has been thoroughly debunked are all bought and paid for by the vaccine industry. 
They are lying and being paid to do it!
And anyone who speaks against them gets royally defamed and defaced by the vaccine industry controlled media.
Andrew Wakefield’s colleague who co-authored the MMR study that linked the MMR vaccine to autism,  has been exonerated and his studies have been confirmed. 
“Justice Mitting, reviewing Dr. Walker-Smith’s appeal in the High Court of Justice, Queen’s Bench Division, Administrative Court, found that the GMC’s conclusions were “based on inadequate and superficial reasoning” and that “the finding of serious professional misconduct and the sanction of erasure are both quashed.”
See full text of the decision.
Dr. Walker-Smith’s professional insurance coverage paid for his appeal; Dr. Wakefield’s insurance carrier would not.
Dr. Wakefield has recently filed a defamation lawsuit in Texas against the British Medical Journal, Dr. Fiona Godlee, Editor-in-Chief, and journalist Brian Deer, who instigated the GMC prosecution. 
His lawsuit alleges that the defendants knowingly or recklessly engaged in fraudulent misrepresentations about 1998 Lancet study.
While far from decisive, the Mitting ruling bodes well for Dr. Wakefield’s defamation action.” 
Read more here
A CDC whistleblower recently admitted that he was forced to withhold vital information from the CDC’s findings on autism. 
CDC Whistleblower admits that the MMR causes autism
Furthermore, there are literally hundreds of independent studies that prove vaccines cause autism. 
Here are some links to studies that are undeniable.
Pro-vaxxer’s eyes seem to gloss over as they see all this proof and they start criticizing the source and everything to keep from seeing the truth!
WAKE UP!
Vaccines DO cause autism!
'''

txt2 = '''
Childhood vaccines protect children from a variety of serious or potentially fatal diseases, including diphtheria, measles, polio and whooping cough (pertussis).
If these diseases seem uncommon — or even unheard of — it's usually because these vaccines are doing their job.
Still, you might wonder about the benefits and risks of childhood vaccines.
Here are straight answers to common questions about childhood vaccines.
A natural infection might provide better immunity than vaccination — but there are serious risks. 
For example, a natural chickenpox (varicella) infection could lead to pneumonia.
A natural polio infection could cause permanent paralysis.
A natural mumps infection could lead to deafness.
A natural Haemophilus influenzae type b (Hib) infection could result in permanent brain damage.
Vaccination can help prevent these diseases and their potentially serious complications.
Vaccines do not cause autism.
Despite much controversy on the topic, researchers haven't found a connection between autism and childhood vaccines.
In fact, the original study that ignited the debate years ago has been retracted. 
'''
#print get_dep_for_sent()
def compare_pages(page1,page2):
    "Takes in two pages and prints out all the conflicting sentences."
    
    d1_dict = doc_to_dict(page1)
    d2_dict = doc_to_dict(page2)
    
    for sent1 in d1_dict:
        for sent2 in d2_dict:
            if conflict2(d1_dict[sent1],d2_dict[sent2]) or conflict(d1_dict[sent1],d2_dict[sent2]):
                print("CONFLICT!: \n  "+sent1+"\n  "+sent2+"\n")

compare_pages(txt1,txt2)
compare_pages("Marijuana is healthy.","Marijuana is not healthy.")

'''
CONFLICT!: 
  furthermore, there are literally hundreds of independent studies that prove vaccines cause autism.
  vaccines do not cause autism.

CONFLICT!: 
  there is absolutely undeniable scientific proof that vaccines cause autism.
  vaccines do not cause autism.

CONFLICT!: 
  marijuana is healthy.
  marijuana is not healthy.
'''