import React, { useState } from "react";
import axios from "axios";

export default function MassaBancaria() {
  const [quantidade, setQuantidade] = useState(10);
  const [permitirNegativo, setPermitirNegativo] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  const gerar = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErro("");
    setResultado(null);
    try {
      const form = new FormData();
      form.append("quantidade", quantidade);
      form.append("permitir_negativo", permitirNegativo);
      const resp = await axios.post("http://localhost:8000/gerar-massa-bancaria/", form);
      setResultado(resp.data.massa_bancaria);
    } catch (err) {
      setErro("Erro ao gerar massa bancária.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Gerar Massa Bancária</h2>
      <form onSubmit={gerar}>
        <label>Quantidade:
          <input type="number" min={1} max={100} value={quantidade} onChange={e => setQuantidade(e.target.value)} style={{ width: 80, marginLeft: 8 }} />
        </label>
        <br/>
        <label>
          <input type="checkbox" checked={permitirNegativo} onChange={e => setPermitirNegativo(e.target.checked)} />
          Permitir saldo negativo
        </label>
        <br/>
        <button type="submit" disabled={loading} style={{ marginTop: 16 }}>
          {loading ? "Gerando..." : "Gerar Massa Bancária"}
        </button>
      </form>
      {erro && <div style={{ color: "red", marginTop: 16 }}>{erro}</div>}
      {resultado && (
        <div style={{ marginTop: 24 }}>
          <strong>Resultado:</strong>
          <pre style={{ background: "#f4f4f4", padding: 12 }}>{JSON.stringify(resultado, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
