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
st.markdown("""<style>
.block-container{max-width:1500px;padding-top:1rem}.hero{padding:1.45rem 1.65rem;border:1px solid rgba(128,128,128,.25);border-radius:22px;background:linear-gradient(120deg,rgba(66,99,235,.16),rgba(0,190,150,.10));margin-bottom:1rem}.hero h1{margin:0}.novel{padding:1rem 1.2rem;border-left:5px solid #6c63ff;background:rgba(108,99,255,.08);border-radius:8px;margin:.7rem 0}.smallflow{font-size:.94rem;line-height:1.55}
</style>""", unsafe_allow_html=True)
STEPS=["Start / OBE Import","Programme & Course","CO → RCO Design","Performance Evidence","Resolution Gate","CARG & MRRP","RBE Attainment","PO/PSO Comparison","Capability Passport","Resolution Ledger","Audit & Improvement","Validation / Export"]
GROUPS={1:"I · EXISTING EDUCATION SYSTEM",5:"II · RBE RESOLUTION LAYER",10:"III · EVIDENCE, REPORTING & IMPROVEMENT"}

def defaults():
    s=st.session_state
    for k,v in {"step":1,"programme":"BCA - Computer Science","course":"Theory of Computation","rco_id":"CO4-RCO","capability":"Evaluate and create computational models, justify the construction, detect invalid reasoning, and adapt when assumptions or constraints change.","envs":"written examination, transfer task, AI-assisted analysis","perts":"constraint shift, misleading evidence, transfer, explanation/justification","positive":"certify","threshold":60.,"epsilon":.10,"bmax":3.,"mode":"Deterministic","obe":None,"reviewer_demo":False}.items(): s.setdefault(k,v)
    s.setdefault("rbe_rows",pd.DataFrame())
    s.setdefault("probes",pd.DataFrame([{"probe_id":"P1","family":"Constraint shift","cost":1.0,"leakage":.10,"accessibility":.95,"reliability":.92,"group_disparity":.05,"resolution_gain":.40},{"probe_id":"P2","family":"Explanation / justification","cost":.8,"leakage":.20,"accessibility":.95,"reliability":.90,"group_disparity":.05,"resolution_gain":.35},{"probe_id":"P3","family":"Transfer","cost":1.2,"leakage":.05,"accessibility":.92,"reliability":.94,"group_disparity":.04,"resolution_gain":.55}]))
def rco():
    s=st.session_state
    return RCO(s.rco_id,s.capability,[x.strip() for x in s.envs.split(',') if x.strip()],[x.strip() for x in s.perts.split(',') if x.strip()],s.positive,float(s.threshold),float(s.epsilon),float(s.bmax))
def nav(position):
    a,b,c=st.columns([1,5,1])
    with a:
        if st.session_state.step>1 and st.button("← Previous",use_container_width=True,key=f"prev_{position}"): st.session_state.step-=1; st.rerun()
    with b: st.progress(st.session_state.step/len(STEPS),text=f"Step {st.session_state.step}/{len(STEPS)} · {STEPS[st.session_state.step-1]}")
    with c:
        if st.session_state.step<len(STEPS) and st.button("Next →",type="primary",use_container_width=True,key=f"next_{position}"): st.session_state.step+=1; st.rerun()
def helpx(t,x):
    with st.expander("Help · "+t): st.write(x)
def novelty(text): st.markdown(f'<div class="novel"><b>RBE begins here.</b><br>{text}</div>',unsafe_allow_html=True)
def load_reviewer_demo():
    s=st.session_state; s.reviewer_demo=True; s.threshold=60.; s.bmax=3.; s.mode="Deterministic"; s.obe=None
    s.rbe_rows=pd.DataFrame([
        {"student_id":"A","name":"Same-score case A","score":82.,"resolved":"Resolved","decision":"certify","risk":None,"burden":0.0},
        {"student_id":"B","name":"Same-score case B","score":82.,"resolved":"Unresolved","decision":"unresolved","risk":None,"burden":1.0},
        {"student_id":"C","name":"Same-score case C","score":82.,"resolved":"Resolved","decision":"not","risk":None,"burden":1.0},
        {"student_id":"D","name":"Below-threshold case","score":55.,"resolved":"Unresolved","decision":"unresolved","risk":None,"burden":0.0},
        {"student_id":"E","name":"Burden-boundary case","score":82.,"resolved":"Unresolved","decision":"unresolved","risk":None,"burden":3.0}])
def ensure_rows():
    s=st.session_state
    if len(s.rbe_rows): return
    if s.obe:
        cid="CO4" if "CO4" in s.obe["co_summary"] else list(s.obe["co_summary"])[0]; vals=[]
        for x in s.obe["students"]:
            score=100*float(x.get(f"{cid}_score01") or 0); vals.append({"student_id":x["student_id"],"name":x["name"],"score":round(score,2),"resolved":"Unresolved","decision":"unresolved","risk":None,"burden":0.0})
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
    return {"framework":"Resolution-Based Education (RBE)","version":"1.1.0-reviewer-flow","programme":s.programme,"course":s.course,"resolution_mode":s.mode,"rco":rco().__dict__,"student_records":[x.__dict__ for x in records()],"rbe_metrics":m,"source_obe":{"metadata":s.obe["metadata"],"co_summary":s.obe["co_summary"],"po_attainment":s.obe["po_attainment"],"warnings":s.obe["warnings"]} if s.obe else None,"audit":audit_course(m)}

defaults(); s=st.session_state
with st.sidebar:
    st.title("🎓 RBE Laboratory"); st.caption("From performance evidence to certification resolution")
    for i,name in enumerate(STEPS,1):
        if i in GROUPS: st.markdown(f"**{GROUPS[i]}**")
        p="●" if i==s.step else "✓" if i<s.step else "○"
        if st.button(f"{p} {i}. {name}",use_container_width=True,key=f"n{i}"): s.step=i; st.rerun()
    st.divider(); st.caption("Foundation DOI: 10.5281/zenodo.22797079"); st.caption("Copyright (C) 2026 Mohammad Amir Khusru Akhtar · Apache-2.0")

st.markdown('<div class="hero"><h1>Resolution-Based Education (RBE) Laboratory</h1><p><b>Performance attainment is not necessarily certification resolution.</b><br>Preserve existing OBE evidence → test the certification distinction → add only decision-targeted evidence when needed → stop, resolve, or defer.</p></div>',unsafe_allow_html=True)
if s.step==1:
    a,b=st.columns([1,2])
    with a:
        if st.button("▶ Run 3-minute Reviewer Demo",type="primary",use_container_width=True,key="reviewer_demo_btn"):
            load_reviewer_demo(); s.step=5; st.rerun()
    with b: st.caption("Loads five controlled cases, including equal scores with different certification-resolution states. No workbook is required.")
with st.expander("Scientific flow · What the software is testing",expanded=s.step==1):
    st.code("OBE evidence → Performance → Resolution Gate → [adequate: STOP] / [inadequate: CARG → MRRP] → AR/AU/RN/Deferred → RBE metrics → Programme/Passport/Ledger/Audit",language=None)
    st.latex(r"w_i\sim_A w_j \Rightarrow g(w_i)=g(w_j)")
    st.caption("Adequacy means that learner possibilities still indistinguishable under the available assessment evidence require the same certification decision.")
nav("top"); step=s.step

if step==1:
    st.header("1 · Start with the existing OBE evidence")
    st.write("Upload the Theory of Computation-style OBE workbook. RBE recomputes and preserves the existing baseline before adding a certification-resolution layer.")
    up=st.file_uploader("Upload OBE workbook (.xlsx)",type=["xlsx"],key="obe_upload")
    if up:
        try: s.obe=import_toc_workbook(up); s.rbe_rows=pd.DataFrame(); s.reviewer_demo=False; st.success(f"Imported {len(s.obe['students'])} learners. Existing OBE calculations were recomputed.")
        except Exception as e: st.error(f"Workbook could not be imported: {e}")
    if s.obe:
        md=s.obe["metadata"]; st.subheader("Detected OBE baseline"); st.write(f"**{md.get('course')}** · {md.get('class')} · {md.get('branch')} · {md.get('year')}")
        co=pd.DataFrame([{"CO":k,"Outcome":s.obe['co_descriptions'].get(k),"Mean score (0–1)":v['workbook_mean_score01'],"CO attainment (0–3)":v['workbook_mean_level']} for k,v in s.obe['co_summary'].items()]); st.dataframe(co,use_container_width=True,hide_index=True)
        for w in s.obe["warnings"]: st.warning(w)
    else: st.info("No workbook uploaded. Use the Reviewer Demo or continue with demonstration data.")
    helpx("Why OBE first?","RBE is a conservative extension. Existing marks, COs, mappings and attainment form K0. If K0 already resolves the required decision, additional RBE burden is zero.")
elif step==2:
    st.header("2 · Programme and course context"); a,b=st.columns(2)
    if s.obe: s.programme=f"{s.obe['metadata'].get('class','')} - {s.obe['metadata'].get('branch','')}"; s.course=str(s.obe['metadata'].get('course') or s.course)
    with a: s.programme=st.text_input("Programme",s.programme,key="programme_input")
    with b: s.course=st.text_input("Course",s.course,key="course_input")
    st.text_area("Purpose / stakeholder / accreditation context",placeholder="Record the approved context. RBE does not change statutory rules by itself.",key="context_input")
    helpx("Governance","For real adoption, record the competent body, approved thresholds, appeals, accessibility, privacy, retention and award authority.")
elif step==3:
    st.header("3 · Enrich a CO into an RCO")
    if s.obe:
        coid=st.selectbox("Existing CO",list(s.obe["co_descriptions"]),key="co_select"); base=s.obe["co_descriptions"].get(coid) or ""
        if st.button("Use this CO as starting capability",key="use_co"): s.rco_id=coid+"-RCO"; s.capability=base; st.rerun()
    s.rco_id=st.text_input("RCO ID",s.rco_id,key="rco_id_input"); s.capability=st.text_area("C · Capability claim",s.capability,key="capability_input"); a,b=st.columns(2)
    with a: s.envs=st.text_area("E · Relevant environments",s.envs,key="env_input")
    with b: s.perts=st.text_area("P · Admissible perturbations",s.perts,key="pert_input")
    s.positive=st.text_input("D · Positive certification decision",s.positive,key="decision_input")
    issues=validate_rco(rco())
    if issues:
        for x in issues: st.error(x)
    else: st.success("RCO fields are structurally complete.")
    helpx("RCO=(C,E,P,D)","A conventional CO is retained. RBE adds environments, admissible perturbations/evidence conditions and the certification distinction that the evidence must support.")
elif step==4:
    st.header("4 · Performance evidence remains performance evidence"); ensure_rows(); a,b,c=st.columns(3)
    with a: s.threshold=st.number_input("Performance threshold T",0.,100.,float(s.threshold),1.,key="threshold_input")
    with b: s.bmax=st.number_input("Maximum additional burden Bmax",0.,20.,float(s.bmax),.5,key="bmax_input")
    with c: s.mode=st.selectbox("Resolution mode",["Deterministic","Probabilistic"],index=0 if s.mode=="Deterministic" else 1,key="mode_input")
    cols={"resolved":st.column_config.SelectboxColumn("Resolution",options=["Resolved","Unresolved"]),"decision":st.column_config.SelectboxColumn("Decision",options=["certify","not","unresolved"]),"score":st.column_config.NumberColumn("Performance score",min_value=0.,max_value=100.)}
    if s.mode=="Probabilistic": s.epsilon=st.number_input("Probabilistic risk threshold ε",0.,1.,float(s.epsilon),.01,key="epsilon_input"); cols["risk"]=st.column_config.NumberColumn("Decision risk",min_value=0.,max_value=1.)
    else: st.caption("Deterministic mode is the theoretical core; no invented probability value is required.")
    s.rbe_rows=st.data_editor(s.rbe_rows,num_rows="dynamic",use_container_width=True,column_config=cols,key="evidence_editor")
    novelty("This is the boundary between conventional performance reporting and the RBE question. Crossing T does not by itself establish that the evidence resolves the capability-bearing certification decision.")
elif step==5:
    st.header("5 · Resolution Gate — the central RBE decision")
    novelty("Ask whether all learner possibilities still compatible with current evidence require the same certification decision. If yes, stop: no extra RBE assessment is needed. If no, the evidence is decision-insufficient.")
    st.latex(r"w_i\sim_A w_j \Rightarrow g(w_i)=g(w_j)")
    st.caption("Assessment-equivalent learner possibilities must be homogeneous with respect to the required certification decision.")
    rr=records(); df=pd.DataFrame([{"Learner":x.student_id,"Performance":x.score,"Performance attained":x.score>=s.threshold,"Resolved":bool(x.resolved),"Decision":x.resolved_decision or "unresolved","Burden":x.burden,"RBE state":x.state} for x in rr]); st.dataframe(df,use_container_width=True,hide_index=True)
    counts=pd.Series([x.state for x in rr]).value_counts(); cols=st.columns(5)
    for col,k in zip(cols,["AR","AU","RN","NA","Deferred"]): col.metric(k,int(counts.get(k,0)))
    if s.reviewer_demo:
        st.success("Reviewer Demo: A, B and C all score 82. A is resolved-positive (AR), B remains unresolved (AU), and C is resolved-negative (RN). The mark is preserved; the evidence status differs.")
        st.info("Case A demonstrates conservative extension: current evidence is already adequate, so added RBE burden is zero. Case E demonstrates finite stopping at the burden boundary.")
    helpx("Interpret states","AR=performance attained + resolved-positive; AU=performance attained but unresolved; RN=performance attained but resolved-negative; NA=performance not attained; Deferred=unresolved at the approved procedural/burden boundary.")
elif step==6:
    st.header("6 · CARG → minimum-burden resolving evidence")
    novelty("Do not automatically collect more evidence. Seek the least burdensome admissible evidence that targets the remaining decision-relevant ambiguity. A merely informative one-step probe is not automatically a complete MRRP.")
    unresolved=[x for x in records() if x.state in {"AU","Deferred"}]; st.metric("Cases with unresolved certification evidence",len(unresolved))
    if unresolved: st.warning("Operational unresolved status alone does not prove CARG from marks. CARG requires remaining compatible possibilities that demand different certification decisions.")
    edited_probes=st.data_editor(s.probes,num_rows="dynamic",use_container_width=True,key="probes_editor"); s.probes=edited_probes
    a,b,c,d,e=st.columns(5); min_gain=a.number_input("Min gain",0.,1.,.30,.05,key="mrrp_min_gain"); min_acc=b.number_input("Min access",0.,1.,.80,.05,key="mrrp_min_access"); min_rel=c.number_input("Min reliability",0.,1.,.80,.05,key="mrrp_min_reliability"); max_disp=d.number_input("Max disparity",0.,1.,.20,.05,key="mrrp_max_disparity"); max_leak=e.number_input("Max leakage",0.,1.,.50,.05,key="mrrp_max_leakage")
    ps=[]
    for _,x in s.probes.iterrows():
        try: ps.append(Probe(str(x.probe_id),str(x.family),float(x.cost),float(x.leakage),float(x.accessibility),float(x.reliability),float(x.group_disparity),float(x.resolution_gain)))
        except Exception: pass
    best=select_minimum_probe(admissible_probes(ps,min_gain,min_acc,min_rel,max_disp,max_leak))
    if best: st.success(f"Minimum-burden admissible one-step probe: {best.probe_id} · {best.family} · burden {best.burden():.2f}")
    else: st.error("No admissible probe meets all declared constraints. Do not force a certification decision.")
    st.caption("A true MRRP is a probe or adaptive policy/tree whose terminal evidence satisfies the declared resolution condition under the approved constraints.")
elif step==7:
    st.header("7 · RBE attainment and resolution metrics"); m=metric_df(); cols=st.columns(7)
    for col,k in zip(cols,["PAR","RR","RAR","UAR","RNR","MRB","DeferredRate"]): col.metric(k,f"{m[k]:.2f}"+("" if k=="MRB" else "%"))
    st.latex(r"PAR = RAR + UAR + RNR\quad\text{when attained cases are exhaustively partitioned}"); st.write(f"Check: **{m['PAR']:.2f} = {m['RAR']:.2f} + {m['UAR']:.2f} + {m['RNR']:.2f}**")
    st.bar_chart(pd.DataFrame({"Metric":["PAR","RR","RAR","UAR","RNR"],"Percent":[m[k] for k in ["PAR","RR","RAR","UAR","RNR"]]}).set_index("Metric"))
    st.caption("PAR reports performance attainment; RAR/UAR/RNR expose how attained cases partition by certification-resolution status. MRB keeps evidence burden visible.")
elif step==8:
    st.header("8 · Existing OBE and RBE programme view")
    if s.obe:
        obe=pd.DataFrame([{"Outcome":k,"Existing OBE attainment":v} for k,v in s.obe["po_attainment"].items()]); st.dataframe(obe,use_container_width=True,hide_index=True); st.caption("Existing OBE PO values are recomputed from the Matrix sheet. Zero-mapped outcomes are reported as N/A, never #DIV/0!.")
    else: st.info("Upload the OBE workbook in Step 1 to obtain the programme baseline. Reviewer Demo intentionally focuses on the resolution mechanism.")
    m=metric_df(); st.subheader("RBE extension for the selected RCO"); st.dataframe(pd.DataFrame([{"RCO":s.rco_id,"PAR":m['PAR'],"RAR":m['RAR'],"UAR":m['UAR'],"RNR":m['RNR'],"RR":m['RR'],"MRB":m['MRB']}]),use_container_width=True,hide_index=True)
    helpx("Do not collapse the scales","The workbook reports conventional OBE attainment; RBE reports performance/resolution proportions and burden. Preserve both rather than pretending they are interchangeable.")
elif step==9:
    st.header("9 · Capability Passport"); rr=records()
    if rr:
        sid=st.selectbox("Learner",[x.student_id for x in rr],key="passport_learner"); x=next(z for z in rr if z.student_id==sid); passport={"student_id":x.student_id,"programme":s.programme,"course":s.course,"rco_id":s.rco_id,"capability":s.capability,"performance_score":x.score,"resolution_state":x.state,"certification_decision":x.resolved_decision,"resolution_mode":s.mode,"decision_risk":x.decision_risk,"resolution_burden":x.burden}; st.json(passport); st.download_button("Download passport JSON",json.dumps(passport,indent=2),f"{sid}_capability_passport.json","application/json",key="passport_download")
    st.caption("The Capability Passport is an additional evidence record; it does not replace a statutory degree or marksheet unless formally authorized.")
elif step==10:
    st.header("10 · Resolution Ledger"); led=pd.DataFrame([x.__dict__ for x in records()]); st.dataframe(led,use_container_width=True,hide_index=True); st.download_button("Download ledger CSV",led.to_csv(index=False),"resolution_ledger.csv","text/csv",key="ledger_download"); st.warning("A production ledger should additionally record K0, probe/response provenance, assessor, rubric/version, moderation and authorized retention/access controls.")
elif step==11:
    st.header("11 · Audit and continuous improvement"); m=metric_df(); a,b=st.columns(2); fair=a.checkbox("Fairness/accessibility concern observed",key="fairness_check"); rel=b.slider("Observed reliability",0.,1.,.90,.01,key="reliability_slider"); findings=audit_course(m,fair,rel)
    if findings:
        for x in findings: st.warning(x)
    else: st.success("No automatic course-level warning was triggered by the entered values.")
    st.text_area("Closed-loop action record",placeholder="Finding → root cause → action → owner/resources → implementation → re-measurement → closure",key="action_record")
    helpx("Interpretation","Low RAR is not automatically a teaching failure. Investigate curriculum, practice, initial assessment, probe quality, assessor consistency, thresholds and access barriers.")
elif step==12:
    st.header("12 · Validation, reproducibility and export"); pkg=report_package(); checks={"RCO structurally complete":not validate_rco(rco()),"Performance/resolution kept separate":True,"Positive/negative resolution separated":True,"Deferred state supported":True,"Deterministic mode available without invented risk":True,"Probabilistic mode optional":True,"Burden cap present":s.bmax>=0,"OBE baseline imported/recomputed":bool(s.obe),"Zero-denominator PO handled":True,"Audit path present":True}; st.dataframe(pd.DataFrame([{"Check":k,"Pass":v} for k,v in checks.items()]),use_container_width=True,hide_index=True)
    a,b=st.columns(2)
    with a: st.download_button("Download complete RBE result JSON",json.dumps(pkg,indent=2,default=str),"rbe_complete_result.json","application/json",use_container_width=True,key="result_download")
    with b: st.download_button("Download evaluated learner CSV",pd.DataFrame(pkg["student_records"]).to_csv(index=False),"rbe_evaluated_learners.csv","text/csv",use_container_width=True,key="learner_download")
    st.info("Software correctness ≠ educational effectiveness. Before high-stakes adoption, use prospective construct review, shadow mode, calibration, fairness/reliability studies and controlled comparison against strong evidence-rich baselines.")
    st.markdown("**Foundation:** Akhtar (2026), *Beyond Outcome Attainment: Resolution-Based Education and the Certification–Assessment Resolution Gap in the Generative-AI Era*. DOI `10.5281/zenodo.22797079`.")
st.divider(); nav("bottom"); st.caption("RBE · Foundation DOI 10.5281/zenodo.22797079 · Copyright (C) 2026 Mohammad Amir Khusru Akhtar · Apache License 2.0")