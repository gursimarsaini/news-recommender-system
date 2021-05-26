
import random
import csv

users = 10
articleRank = 0
ProfileData=[]
for i in range(1,users):
    number_of_sessions = random.randint(1,10)
    for j in range(1,number_of_sessions):
        articles=[]
        articleRank = 0
        NoOfArticlesServed= random.randint(10,15)
        for k in range(NoOfArticlesServed):
            articleRank += 1
            while(1):
                ArticleId= random.randint(1,180)
                if ArticleId in articles:
                    continue
                else:
                    articles.append(ArticleId)
                    break
            
            Clicked =random.randint(0,1)
            timeSpent=0
            if Clicked ==1:
                timeSpent=abs(int(random.gauss(60, 20)))
            temp=[i,j,ArticleId,articleRank,Clicked,timeSpent]
            ProfileData.append(temp)
fields=['UserId','SessionId','ArticleId','ArticleRank','Clicked','TimeSpent']
with open('UserProfileData2.csv','w') as f:
    write = csv.writer(f, lineterminator = '\n')
    write.writerow(fields)
    write.writerows(ProfileData)
            
                    
                
                    
                
                
                
