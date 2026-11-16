P='PNBRQKpnbrqk';U=range;N=(31,33,14,18,-31,-33,-14,-18);B=(15,17,-15,-17);R=(1,-1,16,-16);K=B+R
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':20000};T={};X=88172645463393265;Z=[]
for _ in U(1536):X^=X<<7;X^=X>>9;Z+=[X&((1<<64)-1)]
def zh(b,s):
 h=Z[1535] if s else 0
 for i in U(128):
  p=b[i]
  if p!='.':h^=Z[P.find(p)*128+i]
 return h
def atk(b,x,s):
 n='N' if not s else 'n';k='K' if not s else 'k'
 for d in N:
  y=x+d
  if not y&136 and b[y]==n:return 1
 for d in ((15,17) if not s else (-15,-17)):
  y=x+d
  if not y&136 and b[y]==('P' if not s else 'p'):return 1
 for ds,z in ((B,'BQ' if not s else 'bq'),(R,'RQ' if not s else 'rq')):
  for d in ds:
   y=x+d
   while not y&136:
    if b[y]!='.':
     if b[y] in z:return 1
     break
    y+=d
 for d in K:
  y=x+d
  if not y&136 and b[y]==k:return 1
 return 0
def check(b,s):
 k='K' if not s else 'k';return atk(b,b.index(k),not s)
def moves(b,s,c,e):
 for i in U(128):
  p=b[i]
  if i&136 or p=='.' or p.isupper()!= (not s):continue
  q=p.lower();ds=N if q=='n' else B if q=='b' else R if q=='r' else K if q=='q' else (K if q=='k' else ())
  if q=='p':
   d=-16 if not s else 16;y=i+d
   if not y&136 and b[y]=='.':
    yield i,y,('q' if not s else 'Q') if y<16 or y>111 else p
    if i//16==(6 if not s else 1) and b[i+2*d]=='.':yield i,i+2*d,p
   for d in (d-1,d+1):
    y=i+d
    if y&136:continue
    if b[y]!='.' and b[y].isupper()==s:
     yield i,y,('q' if not s else 'Q') if y<16 or y>111 else p
    elif y==e:yield i,y,p
   continue
  for d in ds:
   y=i+d
   while not y&136:
    if b[y]=='.':yield i,y,p
    else:
     if b[y].isupper()==s:yield i,y,p
     break
    if q not in 'brq':break
    y+=d
  if q=='k' and i==(116 if not s else 4) and not atk(b,i,not s):
   for d,r in ((2,1),( -2,2)):
    if c&r and b[i+d//2]=='.' and b[i+d]=='.' and not atk(b,i+d//2,not s):yield i,i+d,p
def play(b,s,c,e,m):
 i,j,p=m;a=b[:];x=a[i];a[i]= '.'
 if x.lower()=='p' and j==e and a[j]=='.':a[j+(16 if not s else -16)]='.'
 a[j]=p
 if x.lower()=='k' and abs(j-i)==2:
  r=j+(1 if j>i else -2);a[j+(-1 if j>i else 1)]=a[r];a[r]='.'
 return a,not s,c,abs(j-i)==32 and i//16==(6 if not s else 1) and j or (-1)
def legal(b,s,c,e):
 for m in moves(b,s,c,e):
  a,t,f,x=play(b,s,c,e,m)
  if not check(a,s):yield m,a,t,f
def ev(b):
 z=0
 for i,p in enumerate(b):
  if p!='.':z+=(1 if p.isupper() else -1)*V[p.lower()]+(1 if p.isupper() else -1)*((i%16-7)**2//4+(7-i//16)**2)
 return z
def q(b,s,a,z,c,e):
 v=(-1 if s else 1)*ev(b)
 if v>=z:return v
 if v>a:a=v
 for m,A,C,E in legal(b,s,c,e):
  if b[m[1]]=='.' and m[0]+( -16 if not s else 16)!=e:continue
  v=-q(A,not s,-z,-a,C,E)
  if v>=z:return v
  if v>a:a=v
 return a
def go(b,s,c,e,d,a=-30000,z=30000):
 h=zh(b,s)
 if (r:=T.get(h)) and r[0]>=d:return r[1]
 if d<1:return q(b,s,a,z,c,e)
 best=-30000
 for m,A,C,E in legal(b,s,c,e):
  v=-go(A,not s,C,E,d-1,-z,-a)
  if v>best:best=v
  if v>a:a=v
  if a>=z:break
 T[h]=(d,best);return best
def search(b,s,c,e,D=3):
 w=None;v=-30000
 for m,A,C,E in legal(b,s,c,e):
  x=-go(A,not s,C,E,D-1,-30000,30000)
  if x>v:v=x;w=m
 return w
def fen(f):
 a=[]
 for r in f.split()[0].split('/'):
  for x in r:a+=['.']*int(x) if x.isdigit() else [x]
  a+=['.']*8
 return a,('w' not in f.split()[1]),sum(1<<i for i,x in enumerate('KQkq') if x in f.split()[2]),int(f.split()[3]) if f.split()[3]!='-' else -1
def out(m):return chr(97+m[0]%16)+str(8-m[0]//16)+chr(97+m[1]%16)+str(8-m[1]//16)+(m[2].lower()if m[1]//16 in(0,7)else'')
import sys
for l in sys.stdin:
 w=l.split()
 if w[0]=='uci':print('uciok')
 elif w[0]=='isready':print('readyok')
 elif w[0]=='position':
  k=2 if w[1]=='fen' else 1
  if w[k]=='startpos':b,s,c,e=fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -');k+=1
  else:b,s,c,e=fen(' '.join(w[k:k+4]));k+=4
  if k<len(w) and w[k]=='moves':
   for u in w[k+1:]:
    m=next((x for x,_,_,_ in legal(b,s,c,e) if out(x)==u),None)
    if m:b,s,c,e=play(b,s,c,e,m)
 elif w[0]=='go':
  d=int(w[w.index('depth')+1]) if 'depth' in w else 3;m=search(b,s,c,e,d);print('bestmove '+(out(m) if m else '0000'))
 elif w[0]=='quit':break
