
import React, { useState } from "react";
import { darkTheme } from "../darkTheme";
import api from "../api";

export default function MassaBancaria() {
  const [quantidade, setQuantidade] = useState(10);
  const [permitirNegativo, setPermitirNegativo] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    setResultado(null);
    setLoading(true);
    try {
      // Usando a instância do axios configurada com baseURL
      const res = await api.post("/api/massa-bancaria", { quantidade });
      setResultado(res.data.resultado || JSON.stringify(res.data, null, 2));
    } catch (err) {
      setErro("Erro ao gerar massa bancária.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={darkTheme.pageBg}>
      <div style={darkTheme.cardStyle}>
        <h2 style={darkTheme.titleStyle}>
          Gerar Massa Bancária
        </h2>
        <form onSubmit={handleSubmit}>
          <label style={darkTheme.labelStyle}>
            Quantidade de contas:
            <input
              type="number"
              min="1"
              value={quantidade}
              onChange={e => setQuantidade(e.target.value)}
              style={darkTheme.inputStyle}
              required
            />
          </label>
          <button
            type="submit"
            style={darkTheme.buttonStyle}
            disabled={loading}
          >
            {loading ? "Gerando..." : "Gerar"}
          </button>
        </form>
        {erro && <div style={darkTheme.erroStyle}>{erro}</div>}
        {resultado && (
          <pre style={darkTheme.preStyle}>{resultado}</pre>
        )}
        <a href="/" style={{ ...darkTheme.linkStyle, marginTop: 18 }}>
          Voltar para Home
        </a>
      </div>
    </div>
  );
}
