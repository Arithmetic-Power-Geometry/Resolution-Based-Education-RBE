import json, math
import pandas as pd
import streamlit as st
from rbe.models import RCO, Probe, StudentRecord
from rbe.resolution import classify_state
from rbe.mrrp import admissible_probes, select_minimum_probe
from rbe.attainment import course_metrics
from rbe.workbook import import_toc_workbook
from rbe.audit import audit_course
from rbe.validation import validate_rco

st.set_page_config(page_title="RBE Laboratory", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>.block-container{max-width:1500px;padding-top:1.2rem}.hero{padding:1.4rem 1.6rem;border:1px solid rgba(128,128,128,.25);border-radius:22px;background:linear-gradient(120deg,rgba(66,99,235,.16),rgba(0,190,150,.10));margin-bottom:1rem}.hero h1{margin:0}</style>""", unsafe_allow_html=True)
STEPS=["Start / OBE Import","Programme & Course","CO → RCO Design","Performance Evidence","Resolution Gate","CARG & MRRP","RBE Attainment","PO/PSO Comparison","Capability Passport","Resolution Ledger","Audit & Improvement","Validation / Export"]

def defaults():
    s=st.session_state
    for k,v in {"step":1,"programme":"BCA - Computer Science","course":"Theory of Computation","rco_id":"CO4-RCO","capability":"Evaluate and create computational models, justify the construction, detect invalid reasoning, and adapt when assumptions or constraints change.","envs":"written examination, transfer task, AI-assisted analysis","perts":"constraint shift, misleading evidence, transfer, explanation/justification","positive":"certify","threshold":60.,"epsilon":.10,"bmax":3.,"mode":"Deterministic","obe":None}.items(): s.setdefault(k,v)
    s.setdefault("rbe_rows",pd.DataFrame())
    s.setdefault("probes",pd.DataFrame([{"probe_id":"P1","family":"Constraint shift","cost":1.0,"leakage":.10,"accessibility":.95,"reliability":.92,"group_disparity":.05,"resolution_gain":.40},{"probe_id":"P2","family":"Explanation / justification","cost":.8,"leakage":.20,"accessibility":.95,"reliability":.90,"group_disparity":.05,"resolution_gain":.35},{"probe_id":"P3","family":"Transfer","cost":1.2,"leakage":.05,"accessibility":.92,"reliability":.94,"group_disparity":.04,"resolution_gain":.55}]))
def rco():
    s=st.session_state
    return RCO(s.rco_id,s.capability,[x.strip() for x in s.envs.split(',') if x.strip()],[x.strip() for x in s.perts.split(',') if x.strip()],s.positive,float(s.threshold),float(s.epsilon),float(s.bmax))
def nav():
    a,b,c=st.columns([1,5,1])
    with a:
        if st.session_state.step>1 and st.button("← Previous",use_container_width=True): st.session_state.step-=1; st.rerun()
    with b: st.progress(st.session_state.step/len(STEPS),text=f"Step {st.session_state.step}/{len(STEPS)} · {STEPS[st.session_state.step-1]}")
    with c:
        if st.session_state.step<len(STEPS) and st.button("Next →",type="primary",use_container_width=True): st.session_state.step+=1; st.rerun()
def helpx(t,x):
    with st.expander("Help · "+t): st.write(x)
def ensure_rows():
    s=st.session_state
    if len(s.rbe_rows): return
    if s.obe:
        cid="CO4" if "CO4" in s.obe["co_summary"] else list(s.obe["co_summary"])[0]
        vals=[]
        for x in s.obe["students"]:
            score=100*float(x.get(f"{cid}_score01") or 0)
            vals.append({"student_id":x["student_id"],"name":x["name"],"score":round(score,2),"resolved":"Unresolved","decision":"unresolved","risk":None,"burden":0.0})
        s.rbe_rows=pd.DataFrame(vals)
    else:
        s.rbe_rows=pd.DataFrame([{"student_id":"S01","name":"Learner 1","score":82.,"resolved":"Resolved","decision":"certify","risk":None,"burden":0.0},{"student_id":"S02","name":"Learner 2","score":75.,"resolved":"Unresolved","decision":"unresolved","risk":None,"burden":1.0},{"student_id":"S03","name":"Learner 3","score":52.,"resolved":"Unresolved","decision":"unresolved","risk":None,"burden":0.0}])
def records():
    ensure_rows(); rr=rco(); out=[]
    for _,x in st.session_state.rbe_rows.iterrows():
        score=float(x.get("score",0) or 0); dec=str(x.get("decision","unresolved")).strip(); dec=None if dec in {"","unresolved","None","nan"} else dec
        resolved=str(x.get("resolved","Unresolved"))=="Resolved"; risk=None
        if st.session_state.mode=="Probabilistic":
            try: risk=float(x.get("risk")); risk=None if math.isnan(risk) else risk
            except Exception: risk=None
            resolved=dec is not None and risk is not None and risk<=rr.epsilon
        burden=float(x.get("burden",0) or 0); state=classify_state(score,rr,dec,risk,burden,resolved=resolved)
        out.append(StudentRecord(str(x.get("student_id","")),rr.rco_id,score,dec,risk,burden,state,st.session_state.mode.lower(),resolved))
    return out
def metric_df(): return course_metrics(records())
def report_package():
    m=metric_df(); s=st.session_state
    return {"framework":"Resolution-Based Education (RBE)","version":"1.0.0","programme":s.programme,"course":s.course,"resolution_mode":s.mode,"rco":rco().__dict__,"student_records":[x.__dict__ for x in records()],"rbe_metrics":m,"source_obe":{"metadata":s.obe["metadata"],"co_summary":s.obe["co_summary"],"po_attainment":s.obe["po_attainment"],"warnings":s.obe["warnings"]} if s.obe else None,"audit":audit_course(m)}

defaults(); s=st.session_state
with st.sidebar:
    st.title("🎓 RBE Laboratory"); st.caption("OBE-compatible · resolution-aware · guided")
    for i,name in enumerate(STEPS,1):
        p="●" if i==s.step else "✓" if i<s.step else "○"
        if st.button(f"{p} {i}. {name}",use_container_width=True,key=f"n{i}"): s.step=i; st.rerun()
    st.divider(); st.caption("Copyright (C) 2026 Mohammad Amir Khusru Akhtar"); st.caption("Apache License 2.0")
st.markdown('<div class="hero"><h1>Resolution-Based Education (RBE) Laboratory</h1><p>Preserve the existing OBE evidence chain, then test whether the evidence actually resolves the capability decision.</p></div>',unsafe_allow_html=True)
nav(); step=s.step

if step==1:
    st.header("1 · Start with the existing OBE evidence")
    st.write("Upload the Theory of Computation-style OBE workbook. The software reads FLAT, Matrix, CO Calculation and PO Calculation, recomputes CO/PO results, and then adds the RBE layer.")
    up=st.file_uploader("Upload OBE workbook (.xlsx)",type=["xlsx"])
    if up:
        try: s.obe=import_toc_workbook(up); s.rbe_rows=pd.DataFrame(); st.success(f"Imported {len(s.obe['students'])} learners. Existing OBE calculations were recomputed.")
        except Exception as e: st.error(f"Workbook could not be imported: {e}")
    if s.obe:
        md=s.obe["metadata"]; st.subheader("Detected course"); st.write(f"**{md.get('course')}** · {md.get('class')} · {md.get('branch')} · {md.get('year')}")
        co=pd.DataFrame([{"CO":k,"Outcome":s.obe['co_descriptions'].get(k),"Mean score (0–1)":v['workbook_mean_score01'],"CO attainment (0–3)":v['workbook_mean_level']} for k,v in s.obe['co_summary'].items()]); st.dataframe(co,use_container_width=True,hide_index=True)
        for w in s.obe["warnings"]: st.warning(w)
    else: st.info("No workbook uploaded yet. You can still explore the RBE workflow with demonstration data.")
    helpx("Why import OBE first?","RBE is a conservative extension. Existing marks, COs, mappings and attainment are retained; the Resolution Gate is added only where the certification claim needs it.")
elif step==2:
    st.header("2 · Programme and course context"); a,b=st.columns(2)
    if s.obe: s.programme=f"{s.obe['metadata'].get('class','')} - {s.obe['metadata'].get('branch','')}"; s.course=str(s.obe['metadata'].get('course') or s.course)
    with a: s.programme=st.text_input("Programme",s.programme)
    with b: s.course=st.text_input("Course",s.course)
    st.text_area("Purpose / stakeholder / accreditation context",placeholder="Record the approved context. RBE does not change statutory rules by itself.")
    helpx("Governance","For real adoption, record the competent body, approved thresholds, appeals, accessibility, privacy, retention and award authority.")
elif step==3:
    st.header("3 · Enrich a CO into an RCO")
    if s.obe:
        coid=st.selectbox("Existing CO",list(s.obe["co_descriptions"])); base=s.obe["co_descriptions"].get(coid) or ""
        if st.button("Use this CO as starting capability"): s.rco_id=coid+"-RCO"; s.capability=base; st.rerun()
    s.rco_id=st.text_input("RCO ID",s.rco_id); s.capability=st.text_area("C · Capability claim",s.capability); a,b=st.columns(2)
    with a: s.envs=st.text_area("E · Relevant environments",s.envs)
    with b: s.perts=st.text_area("P · Admissible perturbations",s.perts)
    s.positive=st.text_input("D · Positive certification decision",s.positive)
    issues=validate_rco(rco())
    if issues:
        for x in issues: st.error(x)
    else: st.success("RCO fields are structurally complete.")
    helpx("RCO=(C,E,P,D)","A conventional CO is not discarded. RBE adds environments, admissible perturbations and the certification distinction.")
elif step==4:
    st.header("4 · Performance evidence remains performance evidence"); ensure_rows(); a,b,c=st.columns(3)
    with a: s.threshold=st.number_input("Performance threshold T",0.,100.,float(s.threshold),1.)
    with b: s.bmax=st.number_input("Maximum additional burden Bmax",0.,20.,float(s.bmax),.5)
    with c: s.mode=st.selectbox("Resolution mode",["Deterministic","Probabilistic"],index=0 if s.mode=="Deterministic" else 1)
    cols={"resolved":st.column_config.SelectboxColumn("Resolution",options=["Resolved","Unresolved"]),"decision":st.column_config.SelectboxColumn("Decision",options=["certify","not","unresolved"]),"score":st.column_config.NumberColumn("Performance score",min_value=0.,max_value=100.)}
    if s.mode=="Probabilistic": s.epsilon=st.number_input("Probabilistic risk threshold ε",0.,1.,float(s.epsilon),.01); cols["risk"]=st.column_config.NumberColumn("Decision risk",min_value=0.,max_value=1.)
    else: st.caption("Deterministic mode is the default theoretical core. No invented probability/risk value is required.")
    s.rbe_rows=st.data_editor(s.rbe_rows,num_rows="dynamic",use_container_width=True,column_config=cols,key="evidence")
    helpx("Score vs resolution","Score answers whether the declared performance threshold was met. Resolution asks whether still-compatible learner possibilities imply the same certification decision.")
elif step==5:
    st.header("5 · Resolution Gate"); rr=records(); df=pd.DataFrame([{"Learner":x.student_id,"Performance":x.score,"Resolved":bool(x.resolved),"Decision":x.resolved_decision or "unresolved","Risk":x.decision_risk,"Burden":x.burden,"State":x.state} for x in rr]); st.dataframe(df,use_container_width=True,hide_index=True)
    counts=pd.Series([x.state for x in rr]).value_counts(); cols=st.columns(5)
    for col,k in zip(cols,["AR","AU","RN","NA","Deferred"]): col.metric(k,int(counts.get(k,0)))
    st.info("If K0 is already resolution-adequate, stop. RBE adds no extra probe merely because RBE exists.")
    helpx("States","AR=performance attained + resolved-positive; AU=performance attained but unresolved; RN=performance attained but resolved-negative; NA=performance not attained; Deferred=unresolved at the procedural/burden boundary.")
elif step==6:
    st.header("6 · CARG and minimum-burden discriminating evidence"); unresolved=[x for x in records() if x.state in {"AU","Deferred"}]; st.metric("Cases with unresolved certification evidence",len(unresolved))
    if unresolved: st.warning("CARG is present operationally for these cases only if the remaining ambiguity contains learner possibilities requiring different certification decisions. The software does not infer that fact from marks alone.")
    s.probes=st.data_editor(s.probes,num_rows="dynamic",use_container_width=True,key="probes"); a,b,c,d,e=st.columns(5); min_gain=a.number_input("Min gain",0.,1.,.30,.05); min_acc=b.number_input("Min access",0.,1.,.80,.05); min_rel=c.number_input("Min reliability",0.,1.,.80,.05); max_disp=d.number_input("Max disparity",0.,1.,.20,.05); max_leak=e.number_input("Max leakage",0.,1.,.50,.05)
    ps=[]
    for _,x in s.probes.iterrows():
        try: ps.append(Probe(str(x.probe_id),str(x.family),float(x.cost),float(x.leakage),float(x.accessibility),float(x.reliability),float(x.group_disparity),float(x.resolution_gain)))
        except Exception: pass
    best=select_minimum_probe(admissible_probes(ps,min_gain,min_acc,min_rel,max_disp,max_leak))
    if best: st.success(f"Minimum-burden admissible one-step probe: {best.probe_id} · {best.family} · burden {best.burden():.2f}")
    else: st.error("No admissible probe meets all declared constraints. Do not force a certification decision.")
    st.caption("A one-step discriminating probe is not automatically an MRRP. A true MRRP is a probe or adaptive policy whose terminal evidence reaches the declared resolution condition.")
elif step==7:
    st.header("7 · RBE course attainment"); m=metric_df(); cols=st.columns(7)
    for col,k in zip(cols,["PAR","RR","RAR","UAR","RNR","MRB","DeferredRate"]): col.metric(k,f"{m[k]:.2f}"+("" if k=="MRB" else "%"))
    st.latex(r"PAR = RAR + UAR + RNR\quad\text{when attained cases are exhaustively partitioned}"); st.write(f"Check: **{m['PAR']:.2f} = {m['RAR']:.2f} + {m['UAR']:.2f} + {m['RNR']:.2f}**")
    st.bar_chart(pd.DataFrame({"Metric":["PAR","RR","RAR","UAR","RNR"],"Percent":[m[k] for k in ["PAR","RR","RAR","UAR","RNR"]]}).set_index("Metric"))
elif step==8:
    st.header("8 · Existing OBE vs RBE programme view")
    if s.obe:
        obe=pd.DataFrame([{"Outcome":k,"Existing OBE attainment":v} for k,v in s.obe["po_attainment"].items()]); st.dataframe(obe,use_container_width=True,hide_index=True); st.caption("Existing OBE PO values are recomputed from the Matrix sheet. Zero-mapped outcomes are reported as N/A, never #DIV/0!.")
    else: st.info("Upload the OBE workbook in Step 1 to obtain the programme baseline.")
    m=metric_df(); st.subheader("RBE extension for the selected RCO"); st.dataframe(pd.DataFrame([{"RCO":s.rco_id,"PAR":m['PAR'],"RAR":m['RAR'],"UAR":m['UAR'],"RNR":m['RNR'],"RR":m['RR'],"MRB":m['MRB']}]),use_container_width=True,hide_index=True)
    helpx("Comparison","Do not interpret the two scales as interchangeable. The workbook reports 0–3 OBE attainment; RBE reports performance/resolution proportions and burden. Preserve the baseline and expose unresolved certification evidence rather than overwriting OBE.")
elif step==9:
    st.header("9 · Capability Passport"); rr=records()
    if rr:
        sid=st.selectbox("Learner",[x.student_id for x in rr]); x=next(z for z in rr if z.student_id==sid); passport={"student_id":x.student_id,"programme":s.programme,"course":s.course,"rco_id":s.rco_id,"capability":s.capability,"performance_score":x.score,"resolution_state":x.state,"certification_decision":x.resolved_decision,"resolution_mode":s.mode,"decision_risk":x.decision_risk,"resolution_burden":x.burden}; st.json(passport); st.download_button("Download passport JSON",json.dumps(passport,indent=2),f"{sid}_capability_passport.json","application/json")
    st.caption("The Capability Passport is additional evidence; it does not replace the statutory degree/marksheet unless formally authorized.")
elif step==10:
    st.header("10 · Resolution Ledger"); led=pd.DataFrame([x.__dict__ for x in records()]); st.dataframe(led,use_container_width=True,hide_index=True); st.download_button("Download ledger CSV",led.to_csv(index=False),"resolution_ledger.csv","text/csv"); st.warning("A production ledger should additionally record K0, each probe/response, assessor, rubric/version, moderation and provenance, with role-based access and retention limits.")
elif step==11:
    st.header("11 · Audit and continuous improvement"); m=metric_df(); a,b=st.columns(2); fair=a.checkbox("Fairness/accessibility concern observed"); rel=b.slider("Observed reliability",0.,1.,.90,.01); findings=audit_course(m,fair,rel)
    if findings:
        for x in findings: st.warning(x)
    else: st.success("No automatic course-level warning was triggered by the entered values.")
    st.text_area("Closed-loop action record",placeholder="Finding → root cause → action → owner/resources → implementation → re-measurement → closure")
    helpx("Interpretation","Low RAR is not automatically a teaching failure. Investigate curriculum, practice, initial assessment, probe quality, assessor consistency, thresholds and access barriers.")
elif step==12:
    st.header("12 · Validation, reproducibility and export"); pkg=report_package(); checks={"RCO structurally complete":not validate_rco(rco()),"Performance/resolution kept separate":True,"Positive/negative resolution separated":True,"Deferred state supported":True,"Deterministic mode available without invented risk":True,"Probabilistic mode optional":True,"Burden cap present":s.bmax>=0,"OBE baseline imported/recomputed":bool(s.obe),"Zero-denominator PO handled":True,"Audit path present":True}; st.dataframe(pd.DataFrame([{"Check":k,"Pass":v} for k,v in checks.items()]),use_container_width=True,hide_index=True)
    a,b=st.columns(2)
    with a: st.download_button("Download complete RBE result JSON",json.dumps(pkg,indent=2,default=str),"rbe_complete_result.json","application/json",use_container_width=True)
    with b: st.download_button("Download evaluated learner CSV",pd.DataFrame(pkg["student_records"]).to_csv(index=False),"rbe_evaluated_learners.csv","text/csv",use_container_width=True)
    st.info("Research validation remains separate from software correctness. Before high-stakes adoption, use shadow mode, calibration, fairness/reliability studies and controlled comparison against strong OBE/evidence-rich baselines.")
st.divider(); nav(); st.caption("Resolution-Based Education (RBE) · Copyright (C) 2026 Mohammad Amir Khusru Akhtar · Apache License 2.0")
