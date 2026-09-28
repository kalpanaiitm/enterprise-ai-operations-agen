"""Local browser demo for fictional tickets; no outbound sending."""
import uuid
from pathlib import Path

import streamlit as st
from langgraph.types import Command

from evals.run_eval import run as run_retrieval_eval
from evals.run_product_eval import run as run_product_eval
from support_agent.workflow import create_graph

st.set_page_config(page_title="IT Support Agent Demo", layout="wide")
st.title("IT Support Operations Agent")
st.caption("Fictional data only · local in-memory state · every draft needs human review · no send action")

if "graph" not in st.session_state:
    st.session_state.graph = create_graph()
if "ticket_id" not in st.session_state:
    st.session_state.ticket_id = None

ticket_tab, eval_tab = st.tabs(["Try a ticket", "Evaluation"])
with ticket_tab:
    with st.form("new_ticket"):
        ticket = st.text_area("Fictional support request", placeholder="My VPN connection fails every morning")
        submitted = st.form_submit_button("Prepare draft")
    if submitted:
        if not 10 <= len(ticket.strip()) <= 2000:
            st.error("Enter 10 to 2,000 characters.")
        else:
            thread_id = str(uuid.uuid4())
            st.session_state.graph.invoke({"ticket": ticket.strip()},
                                          {"configurable": {"thread_id": thread_id}})
            st.session_state.ticket_id = thread_id

    if st.session_state.ticket_id:
        config = {"configurable": {"thread_id": st.session_state.ticket_id}}
        snapshot = st.session_state.graph.get_state(config)
        state = snapshot.values
        pending = snapshot.next == ("review",)
        escalate = state["sensitive"] or not state["evidence"]
        left, right = st.columns(2)
        with left:
            st.subheader("Decision and evidence")
            st.write(f"Category: **{state['category']}**")
            st.write(f"Sensitive flag: **{state['sensitive']}** · Escalation suggested: **{escalate}**")
            st.write(f"Draft mode: **{state['model_used']}**")
            if state["evidence"]:
                for doc in state["evidence"]:
                    with st.expander(f"{doc['id']} — {doc['title']}"):
                        st.write(doc["text"])
                        st.caption(f"TF-IDF score: {doc['score']}")
            else:
                st.warning("No applicable article found. A specialist should assess this request.")
        with right:
            st.subheader("Draft and human review")
            st.text_area("Suggested text", value=state["draft"], height=190, disabled=True)
            if pending:
                with st.form("review"):
                    edited = st.text_area("Edit before approval (optional)")
                    approve = st.form_submit_button("Approve reviewed text")
                    reject = st.form_submit_button("Reject")
                if approve or reject:
                    if approve and edited and not edited.strip():
                        st.error("An edited response cannot be blank.")
                    else:
                        st.session_state.graph.invoke(Command(resume={
                            "approved": approve,
                            "edited_response": edited.strip() if edited.strip() else None,
                        }), config)
                        st.rerun()
            else:
                st.info(f"Review outcome: {state.get('status', 'unknown')}. Nothing was sent.")
                if state.get("final_response"):
                    st.write(state["final_response"])

with eval_tab:
    st.write("These authored fictional cases are development checks, not estimates of real ticket performance.")
    if st.button("Run offline evaluations"):
        sets = [
            ("Development tickets", run_retrieval_eval()),
            ("Challenge tickets", run_retrieval_eval(Path(__file__).resolve().parent.parent / "evals" / "challenge_cases.json")),
        ]
        for label, result in sets:
            st.subheader(label)
            st.write(f"Category {result['category_correct']}/{result['cases']} · "
                     f"Expected article {result['evidence_hits']}/{result['evidence_cases']} · "
                     f"Abstention {result['abstentions']}/{result['abstention_cases']} · "
                     f"Sensitive flag {result['sensitive_detected']}/{result['sensitive_cases']}")
        try:
            product = run_product_eval()
            st.subheader("Workflow cases")
            st.write(f"Escalation {product['escalation_ok']}/{product['cases']} · "
                     f"Draft checks {product['draft_ok']}/{product['cases']} · "
                     f"Human pause {product['review_paused']}/{product['cases']}")
        except RuntimeError as exc:
            st.info(str(exc))
        st.caption("Checks verify expected snippets and citations, not the tone or factual quality of model-written answers.")
