import React, { useState } from "react";
import axios from "axios";

const CAMPOS = ["nome", "email", "cpf", "cnpj", "telefone", "endereco", "data_nascimento", "empresa"];

export default function MassaDados() {
  const [campos, setCampos] = useState(["nome", "email", "cpf"]);
  const [quantidade, setQuantidade] = useState(10);
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
      campos.forEach(c => form.append("campos", c));
      const resp = await axios.post("http://localhost:8000/gerar-massa-dados/", form);
      setResultado(resp.data.massa);
    } catch (err) {
      setErro("Erro ao gerar massa de dados.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Gerar Massa de Dados</h2>
      <form onSubmit={gerar}>
        <label>Campos:<br/>
          <select multiple value={campos} onChange={e => setCampos(Array.from(e.target.selectedOptions, o => o.value))} style={{ width: "100%", minHeight: 80 }}>
            {CAMPOS.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>
        <br/>
        <label>Quantidade:
          <input type="number" min={1} max={100} value={quantidade} onChange={e => setQuantidade(e.target.value)} style={{ width: 80, marginLeft: 8 }} />
        </label>
        <br/>
        <button type="submit" disabled={loading} style={{ marginTop: 16 }}>
          {loading ? "Gerando..." : "Gerar Dados"}
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
