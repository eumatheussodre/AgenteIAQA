import React, { useState } from "react";
import api from "../api";
import { darkTheme } from "../darkTheme";

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
      // endpoint ajustado para backend Express local
      const resp = await api.post("/api/massa-dados", { quantidade, campos });
      if (resp.data && resp.data.massa) {
        setResultado(resp.data.massa);
      } else {
        setErro("Resposta inválida do backend.");
      }
    } catch (err) {
      setErro("Erro ao gerar massa de dados.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={darkTheme.pageBg}>
      <div style={darkTheme.cardStyle}>
        <h2 style={darkTheme.titleStyle}>📊 Gerar Massa de Dados</h2>
        <form onSubmit={gerar}>
          <label style={darkTheme.labelStyle}>Campos:<br/>
            <select multiple value={campos} onChange={e => setCampos(Array.from(e.target.selectedOptions, o => o.value))} style={{ ...darkTheme.inputStyle, minHeight: 80 }}>
              {CAMPOS.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </label>
          <label style={darkTheme.labelStyle}>Quantidade:
            <input type="number" min={1} max={100} value={quantidade} onChange={e => setQuantidade(e.target.value)} style={{ ...darkTheme.inputStyle, width: 100, marginLeft: 8 }} />
          </label>
          <button type="submit" disabled={loading} style={darkTheme.buttonStyle}>
            {loading ? "Gerando..." : "Gerar Dados"}
          </button>
        </form>
        {erro && <div style={darkTheme.erroStyle}>{erro}</div>}
        {resultado && (
          <div style={{ marginTop: 24 }}>
            <strong>Resultado:</strong>
            <pre style={darkTheme.preStyle}>{JSON.stringify(resultado, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

// ...estilos agora via darkTheme...
