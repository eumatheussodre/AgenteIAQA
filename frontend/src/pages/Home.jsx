import React from "react";
import { Link } from "react-router-dom";
import { darkTheme } from "../darkTheme";
import logo from "../assets/logo.svg";

export default function Home() {
  return (
    <div style={{ ...darkTheme.pageBg, animation: "fadeIn 1.2s" }}>
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .logo-anim {
          animation: logoPop 1.2s cubic-bezier(.68,-0.55,.27,1.55);
        }
        @keyframes logoPop {
          0% { transform: scale(0.7); opacity: 0; }
          60% { transform: scale(1.15); opacity: 1; }
          100% { transform: scale(1); }
        }
      `}</style>
      <div style={{ ...darkTheme.cardStyle, padding: 40, boxShadow: "0 8px 32px 0 rgba(80,80,180,0.18)" }}>
        <img src={logo} alt="Logo" width={72} height={72} className="logo-anim" style={{ marginBottom: 18, boxShadow: "0 2px 12px #6366f1a0", borderRadius: "50%" }} />
        <h1 style={{ ...darkTheme.titleStyle, fontSize: 36, letterSpacing: 2 }}>AgenteIAQA</h1>
        <p style={{ color: "#a5b4fc", marginBottom: 32, fontSize: 18 }}>Automatize, gere e teste com IA. <span style={{ color: "#6366f1", fontWeight: 700 }}>Personalizado para você!</span></p>
        <ul style={{
          fontSize: 18,
          listStyle: "none",
          padding: 0,
          margin: 0,
          display: "flex",
          flexDirection: "column",
          gap: 18
        }}>
          <li><Link to="/casos" style={darkTheme.linkStyle}>🧪 Gerar Casos de Teste (IA)</Link></li>
          <li><Link to="/massa" style={darkTheme.linkStyle}>📊 Gerar Massa de Dados</Link></li>
          <li><Link to="/bancaria" style={darkTheme.linkStyle}>🏦 Gerar Massa Bancária</Link></li>
          <li><Link to="/exportar" style={darkTheme.linkStyle}>📑 Exportar Relatório</Link></li>
          <li><Link to="/llama" style={darkTheme.linkStyle}>🤖 Chat com Llama (local)</Link></li>
        </ul>
      </div>
    </div>
  );
}

// ...estilos agora via darkTheme...
