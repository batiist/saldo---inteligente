import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

st.set_page_config(page_title="Saldo Inteligente", page_icon="🧠")
st.title("🧠 Quanto posso gastar por dia?")

saldo = st.number_input("Quanto tenho HOJE? R$", value=1200.0)
salario = st.number_input("Quanto entra até fim do mês? R$", value=0.0)

if "gastos" not in st.session_state:
    st.session_state.gastos = []

hoje = datetime.now()
ultimo = calendar.monthrange(hoje.year, hoje.month)[1]
dias = ultimo - hoje.day + 1
total = saldo + salario - sum([g["valor"] for g in st.session_state.gastos])
por_dia = total / dias if dias > 0 else 0

st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Dias restantes", dias)
c2.metric("Por DIA", f"R$ {por_dia:.2f}")
c3.metric("Saldo real", f"R$ {total:.2f}")

if por_dia < 20:
    st.error(f"🔴 Apertado! Só R$ {por_dia:.2f} por dia")
elif por_dia < 50:
    st.warning(f"🟡 Atenção: R$ {por_dia:.2f} por dia")
else:
    st.success(f"🟢 De boa! R$ {por_dia:.2f} por dia")

st.divider()
tipo = st.selectbox("Tipo de gasto", ["Débito","Crédito","Pix","Almoço","Gasolina","Stream"])
valor = st.number_input("Valor gasto R$", value=0.0)
desc = st.text_input("Onde gastou?")

if st.button("Adicionar gasto"):
    st.session_state.gastos.append({"tipo": tipo, "valor": valor, "desc": desc})
    st.rerun()

if st.session_state.gastos:
    st.dataframe(pd.DataFrame(st.session_state.gastos))
