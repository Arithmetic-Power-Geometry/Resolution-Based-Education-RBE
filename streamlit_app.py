from pathlib import Path
import json
import math
import pandas as pd
import streamlit as st

from rbe.models import RCO, Probe, StudentRecord
from rbe.resolution import classify_state
from rbe.mrrp import admissible_probes, select_minimum_probe
from rbe.attainment import course_metrics, programme_metrics
from rbe.audit import audit_course

st.set_page_config(page_title="Resolution-Based Education (RBE) Lab", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

st.markdown('''
<style>
.block-container {padding-top: 1.3rem; padding-bottom: 3rem; max-width: 1450px;}
[data-testid="stSidebar"] {border-right: 1px solid rgba(128,128,128,.20);}
.hero {padding: 1.45rem 1.6rem; border-radius: 22px; background: linear-gradient(120deg, rgba(70,80,255,.16), rgba(0,190,160,.12)); border: 1px solid rgba(120,120,160,.22); margin-bottom: 1rem;}
.hero h1 {margin: 0 0 .35rem 0; font-size: 2.25rem;}
.hero p {font-size: 1.05rem; margin: 0;}
</style>
''', unsafe_allow_html=True)

DEFAULT_STUDENTS = pd.DataFrame([
    {"student_id":"S01","score":82.0,"decision":"certify","risk":0.04,"burden":0.5},
    {"student_id":"S02","score":75.0,"decision":"certify","risk":0.08,"burden":1.0},
    {"student_id":"S03","score":71.0,"decision":"unresolved","risk":0.28,"burden":1.2},
    {"student_id":"S04","score":66.0,"decision":"not","risk":0.06,"burden":1.4},
    {"student_id":"S05","score":58.0,"decision":"unresolved","risk":0.50,"burden":0.0},
])
DEFAULT_PROBES = pd.DataFrame([
    {"probe_id":"P1","family":"transfer","cost":1.0,"leakage":0.10,"accessibility":0.95,"reliability":0.92,"group_disparity":0.05,"resolution_gain":0.40},
    {"probe_id":"P2","family":"oral defence","cost":0.8,"leakage":0.35,"accessibility":0.90,"reliability":0.90,"group_disparity":0.08,"resolution_gain":0.38},
    {"probe_id":"P3","family":"constraint shift","cost":1.2,"leakage":0.05,"accessibility":0.92,"reliability":0.94,"group_disparity":0.04,"resolution_gain":0.55},
])
STEPS=[("1","Programme Context"),("2","RCO Design"),("3","Assessment Evidence"),("4","Resolution Gate"),("5","MRRP / Adaptive Probe"),("6","Course Attainment"),("7","Programme Mapping"),("8","Capability Passport"),("9","Resolution Ledger"),("10","Audit & Continuous Improvement"),("11","Export / Test Report")]

def init():
    s=st.session_state
    defaults={"step":1,"programme":"B.Tech. Computer Science and Engineering","course":"Theory of Computation","rco_id":"TOC-RCO4","capability":"Construct and justify computational models, diagnose invalid reasoning, and adapt under changed constraints.","environments":"written exam, transfer task, AI-assisted analysis","perturbations":"constraint shift, misleading evidence, transfer","positive_decision":"certify","threshold":60.0,"epsilon":0.10,"burden_max":3.0,"min_gain":0.30,"min_access":0.80,"min_rel":0.80,"max_disp":0.20,"max_leak":0.50,"notes":""}
    for k,v in defaults.items(): s.setdefault(k,v)
    s.setdefault("students",DEFAULT_STUDENTS.copy()); s.setdefault("probes",DEFAULT_PROBES.copy())
    s.setdefault("mapping",pd.DataFrame([{"rco_id":"TOC-RCO4","PO1":2.0,"PO2":3.0,"PO5":2.0}]))

def current_rco():
    s=st.session_state
    return RCO(s.rco_id,s.capability,[x.strip() for x in s.environments.split(",") if x.strip()],[x.strip() for x in s.perturbations.split(",") if x.strip()],s.positive_decision,float(s.threshold),float(s.epsilon),float(s.burden_max))

def records():
    rr=current_rco(); out=[]
    for _,row in st.session_state.students.iterrows():
        d=str(row.get("decision","unresolved")).strip(); d=None if d.lower() in {"","none","unresolved","nan"} else d
        try:
            risk=float(row.get("risk",1)); risk=None if math.isnan(risk) else risk
        except Exception: risk=None
        score=float(row.get("score",0)); burden=float(row.get("burden",0)); state=classify_state(score,rr,d,risk,burden)
        out.append(StudentRecord(str(row.get("student_id","")),rr.rco_id,score,d,risk,burden,state))
    return out

def metrics(): return course_metrics(records())
def helpbox(title,text):
    with st.expander("💡 Help — "+title): st.write(text)
def nav():
    a,b,c=st.columns([1,4,1])
    with a:
        if st.session_state.step>1 and st.button("← Previous",use_container_width=True): st.session_state.step-=1; st.rerun()
    with b: st.progress(st.session_state.step/len(STEPS),text=f"Step {st.session_state.step} of {len(STEPS)} · {STEPS[st.session_state.step-1][1]}")
    with c:
        if st.session_state.step<len(STEPS) and st.button("Next →",type="primary",use_container_width=True): st.session_state.step+=1; st.rerun()

init()
with st.sidebar:
    st.title("🎓 RBE Lab"); st.caption("Guided implementation · no step is hidden")
    for n,name in STEPS:
        i=int(n); prefix="●" if i==st.session_state.step else ("✓" if i<st.session_state.step else "○")
        if st.button(f"{prefix} {n}. {name}",use_container_width=True,key=f"side_{n}"): st.session_state.step=i; st.rerun()
    st.divider(); st.caption("Copyright (C) 2026 Mohammad Amir Khusru Akhtar"); st.caption("Apache License 2.0")

st.markdown('<div class="hero"><h1>Resolution-Based Education (RBE) Interactive Lab</h1><p>Move from programme intent to resolvable capability, evidence, certification resolution, attainment, programme mapping, audit and export — one guided step at a time.</p></div>',unsafe_allow_html=True)
nav(); step=st.session_state.step; s=st.session_state

if step==1:
    st.header("1 · Programme Context"); st.write("Start with the educational context. These fields become the context for later RCOs, reports and audit records.")
    a,b=st.columns(2)
    with a: s.programme=st.text_input("Programme",s.programme)
    with b: s.course=st.text_input("Course / learning unit",s.course)
    s.notes=st.text_area("Purpose / context notes",s.notes,placeholder="What capability should this course contribute to, and why does it matter?")
    helpbox("Programme Context","Keep the existing programme/course architecture; RBE adds explicit certification-resolution information.")
elif step==2:
    st.header("2 · Design a Resolvable Capability Outcome (RCO)"); st.write("Make capability, environments, perturbations and certification decision explicit.")
    s.rco_id=st.text_input("RCO ID",s.rco_id); s.capability=st.text_area("C — Capability",s.capability); a,b=st.columns(2)
    with a: s.environments=st.text_area("E — Environments (comma separated)",s.environments)
    with b: s.perturbations=st.text_area("P — Perturbations (comma separated)",s.perturbations)
    s.positive_decision=st.text_input("D — Positive certification decision",s.positive_decision); st.code(f"RCO = (C, E, P, D)\nID = {s.rco_id}",language=None)
    helpbox("RCO","Write an evidence-capable capability, relevant contexts, fair perturbations and the certification decision the evidence must support.")
elif step==3:
    st.header("3 · Enter Assessment Evidence"); st.write("Performance evidence and certification evidence remain separate. Edit or paste rows.")
    a,b,c=st.columns(3)
    with a: s.threshold=st.number_input("Performance threshold T",0.,100.,float(s.threshold),1.)
    with b: s.epsilon=st.number_input("Resolution-risk threshold ε",0.,1.,float(s.epsilon),.01)
    with c: s.burden_max=st.number_input("Maximum resolution burden Bmax",0.,20.,float(s.burden_max),.5)
    s.students=st.data_editor(s.students,num_rows="dynamic",use_container_width=True,column_config={"decision":st.column_config.SelectboxColumn("Current decision",options=["certify","not","unresolved"]),"risk":st.column_config.NumberColumn("Decision risk",min_value=0.,max_value=1.,format="%.3f")},key="student_editor")
    helpbox("Evidence","A high score does not automatically resolve certification. Use unresolved when current evidence cannot justify the required decision.")
elif step==4:
    st.header("4 · Resolution Gate"); rr=records(); df=pd.DataFrame([{"student_id":x.student_id,"score":x.score,"decision":x.resolved_decision or "unresolved","risk":x.decision_risk,"burden":x.burden,"RBE_state":x.state} for x in rr]); st.dataframe(df,use_container_width=True,hide_index=True)
    counts=pd.Series([x.state for x in rr]).value_counts(); cols=st.columns(5)
    for col,state in zip(cols,["AR","AU","RN","NA","Deferred"]): col.metric(state,int(counts.get(state,0)))
    helpbox("Resolution Gate","AR=attained and resolved-positive; AU=performance attained but unresolved; RN=performance attained but resolved-negative; NA=not attained; Deferred=unresolved at burden boundary.")
elif step==5:
    st.header("5 · Minimum Resolution-Restoring Perturbation (MRRP)"); st.write("Define candidate probes and constraints. The app filters candidates and selects minimum burden among admissible probes.")
    s.probes=st.data_editor(s.probes,num_rows="dynamic",use_container_width=True,key="probe_editor"); a,b,c,d,e=st.columns(5)
    with a: s.min_gain=st.number_input("Min gain",0.,1.,float(s.min_gain),.05)
    with b: s.min_access=st.number_input("Min access",0.,1.,float(s.min_access),.05)
    with c: s.min_rel=st.number_input("Min reliability",0.,1.,float(s.min_rel),.05)
    with d: s.max_disp=st.number_input("Max disparity",0.,1.,float(s.max_disp),.05)
    with e: s.max_leak=st.number_input("Max leakage",0.,1.,float(s.max_leak),.05)
    probes=[]
    for _,x in s.probes.iterrows():
        try: probes.append(Probe(str(x.probe_id),str(x.family),float(x.cost),float(x.leakage),float(x.accessibility),float(x.reliability),float(x.group_disparity),float(x.resolution_gain)))
        except Exception: pass
    good=admissible_probes(probes,s.min_gain,s.min_access,s.min_rel,s.max_disp,s.max_leak); best=select_minimum_probe(good)
    if best: st.success(f"Recommended next probe: **{best.probe_id} · {best.family}** | burden={best.burden():.2f} | gain={best.resolution_gain:.2f}")
    else: st.warning("No candidate satisfies all constraints. Revise the probe library or thresholds; do not force a certification decision.")
    helpbox("MRRP","This is a one-step constrained selector. A full adaptive MRRP is a policy/tree whose terminal leaves satisfy the stopping condition.")
elif step==6:
    st.header("6 · Course-Level RBE Attainment"); m=metrics(); cols=st.columns(6)
    for col,k in zip(cols,["PAR","RR","RAR","UAR","RNR","MRB"]): col.metric(k,f"{m[k]:.2f}"+("%" if k!="MRB" else ""))
    st.latex(r"\mathrm{PAR}=\mathrm{RAR}+\mathrm{UAR}+\mathrm{RNR}"); st.write(f"Observed: **{m['PAR']:.2f} = {m['RAR']:.2f} + {m['UAR']:.2f} + {m['RNR']:.2f}**")
    st.bar_chart(pd.DataFrame({"Metric":["PAR","RR","RAR","UAR","RNR"],"Percent":[m[k] for k in ["PAR","RR","RAR","UAR","RNR"]]}).set_index("Metric")); helpbox("Metrics","PAR=performance attainment; RR=resolution; RAR=positive resolved attainment; UAR=unresolved attainment; RNR=resolved-negative among performance-attained cases; MRB=mean resolution burden.")
elif step==7:
    st.header("7 · Programme Mapping"); st.write("Map the current RCO to programme outcomes using your institution's mapping convention."); mapping=s.mapping.copy()
    if len(mapping): mapping.loc[:,"rco_id"]=s.rco_id
    s.mapping=st.data_editor(mapping,num_rows="dynamic",use_container_width=True,key="map_editor"); m=metrics(); md={}
    for _,row in s.mapping.iterrows():
        rid=str(row.get("rco_id",s.rco_id)); md.setdefault(rid,{})
        for k,v in row.items():
            if k!="rco_id":
                try: md[rid][str(k)]=float(v)
                except Exception: pass
    pm=programme_metrics([{"rco_id":s.rco_id,**m}],md)
    if pm: st.dataframe(pd.DataFrame(pm).T.reset_index(names="Programme Outcome"),use_container_width=True,hide_index=True)
    helpbox("Programme Mapping","Weighted aggregation supports OBE compatibility. Complex programme capabilities should also use direct programme-level evidence where appropriate.")
elif step==8:
    st.header("8 · Capability Passport"); rr=records()
    if rr:
        sid=st.selectbox("Select learner",[x.student_id for x in rr]); x=next(v for v in rr if v.student_id==sid); a,b,c,d=st.columns(4); a.metric("Score",f"{x.score:.1f}"); b.metric("State",x.state); c.metric("Decision",x.resolved_decision or "unresolved"); d.metric("Burden",f"{x.burden:.2f}")
        passport={"student_id":x.student_id,"programme":s.programme,"course":s.course,"rco_id":s.rco_id,"capability":s.capability,"performance_score":x.score,"resolution_state":x.state,"certification_decision":x.resolved_decision,"decision_risk":x.decision_risk,"resolution_burden":x.burden}; st.json(passport); st.download_button("Download Capability Passport JSON",json.dumps(passport,indent=2),file_name=f"{sid}_RBE_passport.json",mime="application/json")
    helpbox("Capability Passport","A transparent capability summary. Production deployments should apply role-based visibility and data minimization.")
elif step==9:
    st.header("9 · Resolution Ledger"); rr=records(); ledger=pd.DataFrame([{"student_id":x.student_id,"rco_id":x.rco_id,"score":x.score,"decision":x.resolved_decision or "unresolved","risk":x.decision_risk,"burden":x.burden,"state":x.state} for x in rr]); st.dataframe(ledger,use_container_width=True,hide_index=True); st.download_button("Download Resolution Ledger CSV",ledger.to_csv(index=False),"resolution_ledger.csv","text/csv"); helpbox("Resolution Ledger","Production use should add provenance, moderation, appeals, retention controls and approved access policies.")
elif step==10:
    st.header("10 · Audit & Continuous Improvement"); m=metrics(); a,b=st.columns(2)
    with a: fairness=st.checkbox("Flag a fairness/accessibility concern")
    with b: rel=st.slider("Observed assessor/probe reliability",0.,1.,.90,.01)
    for f in audit_course(m,fairness,rel): st.warning(f)
    st.text_area("What should change in curriculum, assessment, probe design, calibration or policy?",placeholder="Record improvement action, owner, evidence required and review point."); helpbox("Continuous Improvement","Use unresolved attainment, burden, reliability and fairness findings to redesign teaching, initial assessment and probe libraries, then retest the next cycle.")
elif step==11:
    st.header("11 · Export, Reproduce and Test"); rr=records(); m=metrics(); package={"framework":"Resolution-Based Education (RBE)","programme":s.programme,"course":s.course,"rco":{"id":s.rco_id,"capability":s.capability,"environments":[x.strip() for x in s.environments.split(",") if x.strip()],"perturbations":[x.strip() for x in s.perturbations.split(",") if x.strip()],"positive_decision":s.positive_decision,"threshold":s.threshold,"epsilon":s.epsilon,"burden_max":s.burden_max},"records":[x.__dict__ for x in rr],"course_metrics":m,"audit":audit_course(m)}; st.success("The complete guided workflow has reached the export stage."); st.json(package,expanded=False); a,b=st.columns(2)
    with a: st.download_button("Download Complete RBE Result JSON",json.dumps(package,indent=2),"rbe_result.json","application/json",use_container_width=True)
    with b: st.download_button("Download Evaluated Learners CSV",pd.DataFrame(package["records"]).to_csv(index=False),"rbe_evaluated_learners.csv","text/csv",use_container_width=True)
    st.info("For high-stakes use, locally validate thresholds, decision models, probe effects, fairness, reliability and governance before actual certification.")

st.divider(); nav(); st.caption("Resolution-Based Education (RBE) · Copyright (C) 2026 Mohammad Amir Khusru Akhtar · Apache License 2.0")
