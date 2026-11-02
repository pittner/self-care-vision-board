#!/usr/bin/env python3
"""Builds index.html for pittner/self-care-vision-board.

A single-purpose page for the "self care vision board" / "self care goals 2027" search intent:
36 self-care goals in 6 groups (rest and sleep, body, mind, boundaries, joy, people), each with why
it matters and a first step; one click opens the free maker prefilled as a phone lock screen.
Plus 12 questions, a 45-minute plan, a box for your own goal, and FAQ.
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/self-care-vision-board/"
SRC = "ghpages_selfcare"
CAMPAIGN = "selfcare_2027"

# (group, [(goal, why it matters, a first step for this week)])
GROUPS = [
    ("Rest and sleep", [
        ("Sleep 7 to 8 hours most nights", "Almost everything feels harder on five hours of sleep.", "Set a fixed bedtime alarm 30 minutes before you want to sleep"),
        ("No phone in bed", "The last scroll of the day steals the first hour of sleep.", "Put a charger outside the bedroom tonight"),
        ("Take one real day off every week", "Rest you schedule actually happens; rest you hope for does not.", "Mark one day this week with no work and no chores"),
        ("Have a slow morning routine", "A calm first 20 minutes sets the tone for the whole day.", "Write three things you will do before checking messages"),
        ("Nap without guilt when I need it", "A short rest beats pushing through on empty.", "Try one 20-minute nap this weekend"),
        ("Take a full week of holiday", "Long weekends recharge; a full week resets.", "Pick the week in 2027 and block it in your calendar now"),
    ]),
    ("Body", [
        ("Walk 30 minutes a day", "Walking is the easiest movement you will actually keep.", "Walk for 30 minutes today, no app needed"),
        ("Drink more water", "Mild thirst often feels like tiredness or hunger.", "Put a full bottle on your desk every morning this week"),
        ("Cook at home three times a week", "Home food is cheaper, kinder and slower.", "Plan three simple dinners and buy the ingredients"),
        ("Stretch for 10 minutes every evening", "A little stretching undoes a day of sitting.", "Follow one 10-minute stretch video tonight"),
        ("Book the check-ups I have postponed", "Prevention is the most boring and the most important self care.", "List the doctor, dentist or eye check you are overdue for and call one"),
        ("Move in a way I enjoy", "Exercise you like is exercise you repeat.", "Try one new class or sport this month"),
    ]),
    ("Mind", [
        ("Journal for 5 minutes a day", "Writing a thought down makes it smaller.", "Keep a notebook by your bed and write three lines tonight"),
        ("Meditate or breathe for 10 minutes", "A short pause each day lowers the volume of stress.", "Set a 10-minute timer and just breathe slowly"),
        ("Read for pleasure again", "A book is a rest for the part of you that is always online.", "Pick one novel and read 10 pages before bed"),
        ("Spend less time on social media", "Comparing yourself all day quietly drains you.", "Set a 30-minute daily limit on your most used app"),
        ("Talk to a therapist or coach", "Some knots are easier to untie with help.", "Look up two therapists near you and save their numbers"),
        ("Be kinder to myself when I fail", "You would never talk to a friend the way you talk to yourself.", "Write down one thing you did well this week"),
    ]),
    ("Boundaries", [
        ("Say no without long explanations", "Every yes to something you do not want is a no to yourself.", "Prepare one short polite no sentence and use it this week"),
        ("Stop answering work messages after 7 pm", "Always being reachable means never fully resting.", "Turn on do not disturb from 7 pm every evening"),
        ("Leave relationships that drain me", "Who you spend time with shapes how you feel.", "Notice who leaves you tired this week and write their names down"),
        ("Protect one evening a week for myself", "Time nobody can claim is the base of self care.", "Choose the evening and say it out loud to your household"),
        ("Clear clutter at home", "A calm room makes a calmer head.", "Clear one drawer or one shelf today"),
        ("Keep my money calm", "Money stress is life stress.", "Write down your fixed monthly costs and what is left"),
    ]),
    ("Joy", [
        ("Do one thing just for fun every week", "Fun is not a reward for finishing work; it is fuel.", "Write three things you used to love doing and pick one"),
        ("Start a hobby with my hands", "Making something with your hands quiets the mind.", "Buy the cheapest starter kit for drawing, knitting or pottery"),
        ("Spend time in nature every week", "A walk among trees lowers stress faster than most apps.", "Find the nearest park or forest and go this weekend"),
        ("Take myself on a solo date", "Enjoying your own company is a skill.", "Choose a cafe, museum or cinema and go alone this month"),
        ("Listen to music I love every day", "One song can change the mood of an afternoon.", "Make a short playlist of songs that lift you"),
        ("Learn something just because I am curious", "Learning without pressure feels like play.", "Pick one topic and watch one lesson this week"),
    ]),
    ("People", [
        ("See my closest friends every month", "Time with people who know you is real rest.", "Message one friend today and set a date"),
        ("Call my parents or family more often", "Short regular calls keep people close.", "Put a weekly call reminder in your phone"),
        ("Ask for help when I need it", "Doing everything alone is not strength, it is exhaustion.", "Name one task someone else could take from you this week"),
        ("Spend quality time with my partner", "Couples drift apart in the small busy weeks.", "Plan one phone-free evening together"),
        ("Meet new people who share my interests", "A new circle brings new energy.", "Look up one club, group or class near you"),
        ("Celebrate small wins with someone", "Shared joy grows.", "Tell one person about something good that happened this week"),
    ]),
]

QUESTIONS = [
    "When did I feel most rested in 2026, and why?",
    "What drained my energy most this year?",
    "How many hours do I really sleep on a normal night?",
    "Which habit do I keep promising myself and never start?",
    "Who leaves me feeling better after we meet?",
    "What do I say yes to that I want to say no to?",
    "What did I love doing as a child that I stopped?",
    "Where in my week is there time only for me?",
    "Which check-up or health task have I postponed?",
    "How do I talk to myself when something goes wrong?",
    "What would a perfect slow Sunday look like?",
    "If 2027 goes really well, how do I feel by next December?",
]

PLAN = [
    ("10 minutes: look back honestly.", "Note what gave you energy in 2026 and what took it."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers are enough; nobody else reads them."),
    ("10 minutes: pick three goals.", "Not ten. One for rest, one for your body or mind, one for joy or people."),
    ("10 minutes: make it visible.", "Turn your main self-care goal and its first step into a phone lock screen, so you see it every day."),
]

FAQ = [
    ("What should go on a self care vision board?",
     "Put the goal in your own words, a first step you can do this week, and why it matters to you. "
     "This page has 36 self-care goals in 6 groups (rest and sleep, body, mind, boundaries, joy, people), each with a first step, so you can pick three and make them visible."),
    ("Does a self care vision board actually work?",
     "A board does not rest for you, but seeing the goal every day reminds you to choose it when the week gets busy. "
     "The habit that works best is putting it on your phone lock screen."),
    ("How many self care goals should I set for 2027?",
     "Three is enough: one for rest, one for body or mind, one for joy or people. Fewer goals get kept more often."),
    ("What are good self care goals for busy people?",
     "Small, daily and specific: a fixed bedtime, a 30-minute walk, no work messages after 7 pm. Start with one and add the next when it feels easy."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone lock screen or print it."),
    ("Can I make a full self care vision board with all my goals?",
     "Yes. Start from your goals in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Self Care Vision Board 2027: %%COUNT%% Self-Care Goals with a First Step + Free Lock Screen</title>
<meta name="description" content="%%COUNT%% self-care goals for 2027 (rest and sleep, body, mind, boundaries, joy, people), each with a first step for this week, %%NQ%% questions and a 45-minute plan. Free lock screen maker.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Self care vision board 2027 - %%COUNT%% self-care goals with a first step and a free lock screen">
<meta property="og:description" content="Sleep, boundaries, joy and calm-mind goals with a first step, %%NQ%% questions, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Self care vision board 2027: %%COUNT%% self-care goals with a first step for this week</h1>
  <p class="lede">Self care slips first when life gets busy, because it has no deadline and no first step. Below are %%COUNT%% self-care goals for 2027, from better sleep to saying no, each with why it matters and a first step you can do this week, plus %%NQ%% questions to find out what you really need. Press a goal and it opens in a free maker with the first step under it: save it as your phone lock screen and see it every day until it becomes a habit.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My self-care goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Sleep 8 hours on weeknights" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Phone charger out of the bedroom tonight" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions before you choose your goals</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads it. The answers that surprise you point to the goals that will actually stick.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Plan your self-care year in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full self care vision board</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/money-vision-board/">money vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-weight-loss/">weight loss vision board</a>,
  <a href="https://pittner.github.io/new-year-resolutions-2027/">new year's resolutions 2027</a>,
  <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/self-care-vision-board">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
