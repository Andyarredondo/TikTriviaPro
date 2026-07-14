import React from 'react';
export default function RoundBanner({text='ROUND OPEN'}){
  return <div style={{textAlign:'center',padding:'10px',color:'var(--rrn-gold)',fontWeight:700,letterSpacing:'3px'}}>{text}</div>;
}
