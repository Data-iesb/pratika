import json
import os
import urllib.request
import boto3

GHOST_URL = "https://pratika.dataiesb.com"
GHOST_API_KEY = os.environ["GHOST_API_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]
CF_DISTRIBUTION = os.environ["CF_DISTRIBUTION"]

NAVBAR = '<nav><div class="logo"><a href="https://pratika.blog.br">Prátika</a></div><ul><li><a href="https://pratika.blog.br/#noticias">Notícias</a></li><li><a href="https://pratika.blog.br/#quem-somos">Quem Somos</a></li><li><a href="https://pratika.blog.br/#contato">Fale Conosco</a></li></ul></nav>'

FOOTER = '<footer><p style="font-size:0.85rem"><a href="mailto:gabriela.santos@iesb.br">gabriela.santos@iesb.br</a> | <a href="mailto:larissa.ferraz@iesb.br">larissa.ferraz@iesb.br</a> | <a href="mailto:pratika@iesb.br">pratika@iesb.br</a></p><p style="margin-top:0.5rem;font-size:0.75rem;opacity:0.5">Patrocinado por <a href="https://dataiesb.com">DataIESB</a> e <a href="https://aws.amazon.com">AWS</a> | Desenvolvido por <a href="https://levav.it">Levav-IT</a></p><div class="sponsors"><a href="https://levav.it" target="_blank"><img src="https://www.pratika.blog.br/logos/levav-it.png" alt="Levav-IT" style="height:32px;"></a><a href="https://dataiesb.com" target="_blank"><img src="https://www.pratika.blog.br/logos/iesb.png" alt="DataIESB" style="height:32px;"></a><a href="https://aws.amazon.com" target="_blank"><img src="https://www.pratika.blog.br/logos/aws.svg" alt="AWS" style="height:22px;"></a></div><a href="https://instagram.com/pratikaiesb" target="_blank" style="margin-top:0.5rem;display:inline-block;">@pratikaiesb</a></footer>'

CANVAS_SCRIPT = '''<script>
const canvas=document.getElementById('bg-canvas'),ctx=canvas.getContext('2d');let W,H;
function resize(){W=canvas.width=window.innerWidth;H=canvas.height=document.documentElement.scrollHeight}
window.addEventListener('resize',resize);resize();
function seeded(s){return function(){s=(s*9301+49297)%233280;return s/233280}}
const rng=seeded(42);
const scraps=[];for(let i=0;i<18;i++){scraps.push({x:rng()*W,y:rng()*H,w:40+rng()*80,h:30+rng()*60,rot:(rng()-0.5)*0.4,alpha:0.06+rng()*0.08,drift:(rng()-0.5)*0.3,speed:0.1+rng()*0.2})}
const tapes=[];for(let i=0;i<12;i++){tapes.push({x:rng()*W,y:rng()*H,w:50+rng()*70,h:12+rng()*8,rot:(rng()-0.5)*0.6,alpha:0.12+rng()*0.1,color:rng()>0.5?'rgba(200,190,100,':'rgba(100,180,200,'})}
const clips=[];for(let i=0;i<8;i++){clips.push({x:rng()*W,y:rng()*H,rot:(rng()-0.5)*1.0,size:16+rng()*12,swing:rng()*Math.PI*2})}
const balls=[];for(let i=0;i<6;i++){balls.push({x:rng()*W,y:rng()*H,r:8+rng()*14,vx:(rng()-0.5)*0.4,vy:-0.2-rng()*0.3,alpha:0.08+rng()*0.06})}
function drawTornPaper(s){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(s.rot);ctx.globalAlpha=s.alpha;ctx.fillStyle='#f5f0e8';ctx.beginPath();const steps=12;for(let i=0;i<=steps;i++){const px=(i/steps)*s.w-s.w/2;const py=-s.h/2+(Math.sin(i*1.7)*3);i===0?ctx.moveTo(px,py):ctx.lineTo(px,py)}for(let i=steps;i>=0;i--){const px=(i/steps)*s.w-s.w/2;const py=s.h/2+(Math.cos(i*2.1)*4);ctx.lineTo(px,py)}ctx.closePath();ctx.fill();ctx.restore()}
function drawTape(t){ctx.save();ctx.translate(t.x,t.y);ctx.rotate(t.rot);ctx.globalAlpha=t.alpha;ctx.fillStyle=t.color+t.alpha+')';ctx.fillRect(-t.w/2,-t.h/2,t.w,t.h);ctx.restore()}
function drawClip(c,t){ctx.save();ctx.translate(c.x,c.y);ctx.rotate(c.rot+Math.sin(t*0.5+c.swing)*0.05);ctx.globalAlpha=0.3;ctx.strokeStyle='#888';ctx.lineWidth=2;ctx.beginPath();const s=c.size;ctx.moveTo(0,-s);ctx.lineTo(0,s*0.6);ctx.arc(0,s*0.6,s*0.3,Math.PI,0,true);ctx.lineTo(s*0.3*0.6,-s*0.5);ctx.arc(0,-s*0.5,s*0.3*0.6,0,Math.PI,true);ctx.stroke();ctx.restore()}
let time=0;
function animate(){
time+=0.016;ctx.clearRect(0,0,W,H);
const grad=ctx.createRadialGradient(W/2,H/3,0,W/2,H/3,W);grad.addColorStop(0,'#d44332');grad.addColorStop(1,'#8e1a0e');ctx.fillStyle=grad;ctx.fillRect(0,0,W,H);
ctx.globalAlpha=0.04;ctx.strokeStyle='#000';ctx.lineWidth=1;
for(let i=0;i<8;i++){ctx.beginPath();const sx=rng()*W;ctx.moveTo(sx,0);ctx.quadraticCurveTo(sx+100,H/2,sx-50,H);ctx.stroke()}
ctx.globalAlpha=1;
scraps.forEach(s=>{s.y+=Math.sin(time+s.x)*s.speed;s.x+=Math.cos(time*0.7+s.y*0.01)*s.drift;drawTornPaper(s)});
tapes.forEach(drawTape);
clips.forEach(c=>drawClip(c,time));
balls.forEach(b=>{b.x+=b.vx+Math.sin(time+b.x*0.01)*0.2;b.y+=b.vy;if(b.y<-30)b.y=H+30;if(b.x<-30)b.x=W+30;if(b.x>W+30)b.x=-30;ctx.save();ctx.globalAlpha=b.alpha;ctx.fillStyle='#f5f0e8';ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fill();ctx.restore()});
requestAnimationFrame(animate)}
new ResizeObserver(resize).observe(document.documentElement);
animate();
</script>'''

CSS = """@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Special+Elite&family=Lora:ital,wght@0,400;1,400&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Lora',serif;background:#b5311e;color:#2c2c2c;min-height:100vh;overflow-x:hidden}
nav{background:#f5f0e8;border-bottom:3px solid #2c2c2c;padding:1rem 2rem;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;box-shadow:0 4px 8px rgba(0,0,0,0.3)}
.logo a{font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#c0392b;text-decoration:none;transform:rotate(-2deg);display:inline-block}
nav ul{display:flex;gap:0.5rem;list-style:none}
nav ul li a{font-family:'Special Elite',monospace;text-decoration:none;color:#2c2c2c;padding:0.5rem 1.2rem;background:#fff;border:2px solid #2c2c2c;transition:all 0.2s}
nav ul li a:hover{background:#c0392b;color:#fff;transform:rotate(-1deg)}
.post-content{max-width:800px;margin:0 auto;padding:3rem 2rem;position:relative;z-index:1}
.post-header{background:#f5f0e8;padding:2.5rem 2.5rem 1.5rem;box-shadow:4px 4px 0 rgba(0,0,0,0.25);border:1px solid #d4c9b8;border-bottom:none}
.post-header h1{font-family:'Playfair Display',serif;font-size:2.2rem;color:#c0392b;margin-bottom:0.5rem}
.post-meta{font-family:'Special Elite',monospace;color:#888;font-size:0.9rem}
.post-body{background:#f5f0e8;padding:0 2.5rem 2.5rem;box-shadow:4px 4px 0 rgba(0,0,0,0.25);border:1px solid #d4c9b8;border-top:none;font-family:'Special Elite',monospace;line-height:1.8}
.post-body p{margin-bottom:1rem}
.post-body img{max-width:100%;margin:1rem 0;border:3px solid #2c2c2c;box-shadow:3px 3px 0 rgba(0,0,0,0.2)}
.back-link{display:inline-block;margin-top:2rem;font-family:'Special Elite',monospace;color:#f5f0e8;background:#c0392b;padding:0.5rem 1rem;border:2px solid #2c2c2c;text-decoration:none;transition:transform 0.2s}
.back-link:hover{transform:rotate(-1deg) scale(1.05)}
footer{background:#2c2c2c;color:#f5f0e8;text-align:center;padding:2rem;margin-top:3rem;font-family:'Special Elite',monospace;position:relative;z-index:1}
footer a{color:#f5f0e8;text-decoration:none}
footer a:hover{color:#e74c3c}
.sponsors{display:flex;justify-content:center;align-items:center;gap:2rem;margin-top:1rem}
@media(max-width:600px){nav{flex-direction:column;gap:0.5rem;padding:0.75rem 1rem}.logo a{font-size:1.5rem}nav ul{flex-wrap:wrap;justify-content:center;gap:0.3rem}nav ul li a{font-size:0.7rem;padding:0.4rem 0.6rem}.post-content{padding:1.5rem 1rem}}"""


def get_posts():
    url = f"{GHOST_URL}/ghost/api/content/posts/?key={GHOST_API_KEY}&include=tags,authors&formats=html&limit=all"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read()).get('posts', [])


def fix_urls(text):
    return text.replace('http://app.dataiesb.com', 'https://pratika.dataiesb.com').replace('http://pratika.dataiesb.com', 'https://pratika.dataiesb.com')


def build_page(post):
    title = post['title']
    html_content = fix_urls(post['html'])
    img = fix_urls(post.get('feature_image', '') or '')
    img_tag = f'<img src="{img}" style="max-width:100%;margin-top:1rem;border:3px solid #2c2c2c;box-shadow:3px 3px 0 rgba(0,0,0,0.2)">' if img else ''
    date = post.get('published_at', '')[:10]
    author = post.get('primary_author', {}).get('name', '') if post.get('primary_author') else ''
    meta = f'<div class="post-meta"><span>{date}</span>{" &middot; Por " + author if author else ""}</div>'

    return f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title} - Prátika</title><style>{CSS}#bg-canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none}}</style></head><body><canvas id="bg-canvas"></canvas>{NAVBAR}<div class="post-content"><div class="post-header"><h1>{title}</h1>{meta}{img_tag}</div><div class="post-body">{html_content}</div><a href="https://pratika.blog.br" class="back-link">&larr; Voltar para Notícias</a></div>{FOOTER}{CANVAS_SCRIPT}</body></html>'''


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    cf = boto3.client('cloudfront')

    posts = get_posts()
    paths = []

    for post in posts:
        slug = post['slug']
        html = build_page(post)
        s3.put_object(Bucket=S3_BUCKET, Key=f"{slug}/index.html", Body=html.encode(), ContentType='text/html')
        paths.append(f"/{slug}/*")

    # Update homepage with news from Ghost
    news_items = ''
    for i, post in enumerate(posts):
        slug = post['slug']
        title = post['title']
        date = post.get('published_at', '')[:10]
        excerpt = post.get('excerpt', '')[:120]
        img = fix_urls(post.get('feature_image', '') or '')
        img_tag = f'<img src="{img}" style="max-width:100%;margin-bottom:1rem;border:3px solid #2c2c2c;box-shadow:3px 3px 0 rgba(0,0,0,0.2)">' if img else ''
        active = ' active' if i == 0 else ''
        news_items += f'<a href="/{slug}/" style="text-decoration:none;color:#2c2c2c"><div class="news-item carousel-item{active}">{img_tag}<h3>{title}</h3><p class="date">{date}</p><p style="font-family:\'Special Elite\',monospace;margin-top:0.5rem">{excerpt}</p></div></a>'

    # Get current index.html and inject news
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key='index.html')
        homepage = obj['Body'].read().decode()
        # Replace content between news markers
        import re
        pattern = r'(<h2>Últimas Notícias</h2>\s*<div class="carousel">).*?(</div>\s*<div class="carousel-controls">)'
        replacement = r'\1\n' + news_items + r'\2'
        homepage = re.sub(pattern, replacement, homepage, flags=re.DOTALL)
        s3.put_object(Bucket=S3_BUCKET, Key='index.html', Body=homepage.encode(), ContentType='text/html')
        paths.append('/index.html')
        paths.append('/')
    except Exception as e:
        print(f"Error updating homepage: {e}")

    if paths:
        cf.create_invalidation(
            DistributionId=CF_DISTRIBUTION,
            InvalidationBatch={'Paths': {'Quantity': len(paths), 'Items': paths}, 'CallerReference': str(hash(str(paths)))}
        )

    return {'statusCode': 200, 'body': json.dumps(f'Synced {len(posts)} posts')}
