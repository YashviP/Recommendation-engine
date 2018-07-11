
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.cluster import KMeans

prob_data=pd.read_csv('problem_data.csv')
user_data=pd.read_csv('user_data.csv')
train_data=pd.read_csv('train_submissions.csv')

#print type(train_data)
train=pd.DataFrame.merge(train_data,user_data,on='user_id',left_index=True)
train=pd.DataFrame.merge(train,prob_data,on='problem_id',left_index=True)
#print train.shape

test_data=pd.read_csv('test.csv')
#print test_data.shape
test=pd.DataFrame.merge(test_data,user_data,on='user_id',left_index=True)
test=pd.DataFrame.merge(test,prob_data,on='problem_id',left_index=True)
#print test.shape



            
#print train['country'].value_counts()
train['country'].fillna('India', inplace=True)


#print train['level_type'].value_counts()
train['level_type'].fillna('A', inplace=True)


#print train['points'].value_counts()
train['points'].fillna(500.0, inplace=True)

#print train['tags'].value_counts()
train['tags'].fillna('implementation', inplace=True)

#print train.isnull().sum()

#print train.dtypes

#country tags 

print train['level_type'].value_counts()
train['level_type'] = train['level_type'].map({'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14})
train=pd.get_dummies(train, columns=["rank"])
train=train.drop(['country','tags'],axis=1)

            
#print train['country'].value_counts()
test['country'].fillna('India', inplace=True)


#print train['level_type'].value_counts()
test['level_type'].fillna('A', inplace=True)


#print train['points'].value_counts()
test['points'].fillna(500.0, inplace=True)

#print train['tags'].value_counts()
test['tags'].fillna('implementation', inplace=True)

#print train.isnull().sum()

#print train.dtypes

test['level_type'] = test['level_type'].map({'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14})
test=pd.get_dummies(test, columns=["rank"])
test=test.drop(['country','tags'],axis=1)


target=train['attempts_range']
train_X=train.drop(['user_id','problem_id','attempts_range'],axis=1)


id=test['ID']
test_X=test.drop(['user_id','problem_id','ID'],axis=1)

print train_X.dtypes
print test_X.dtypes

n_classes=len(np.unique(target))

param = {
    'eta': 0.3,  # the training step for each iteration
    'silent': 1,  # logging mode - quiet
    'objective': 'multi:softprob',  # error evaluation for multiclass training
    'num_class': 6 }  # the number of classes that exist in this datset



xgb = XGBClassifier(num_class=6,eta=0.3,silent=1,max_depth=50,learning_rate=0.08,n_estimators=6)
xgb.fit(train_X,target)
output=xgb.predict(test_X)

'''
n_clusters = len(np.unique(target))
clf = KMeans(n_clusters = n_clusters)
clf.fit(train_X)
output=clf.predict(test_X)
'''
my_submission = pd.DataFrame({'ID':id ,'attempts_range': output})
my_submission.to_csv('submission.csv', index=False)



