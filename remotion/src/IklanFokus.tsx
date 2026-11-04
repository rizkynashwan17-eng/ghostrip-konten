// Iklan fokus satu fitur (Cek muatan, Data truk), gaya 3D startup tech yang sama dengan Iklan3D.
import React from 'react';
import {AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {C} from './theme';
import {Chip, Cube, F, Head, IklanProps, Phone, S1Logo, S8CTA, Stage, Sub, Tag, Trans, cl, eo, sp, useOutfit} from './Iklan3D';

const Pill: React.FC<{x: number; y: number; text: string; on?: boolean; delay?: number; color?: string}> = ({x, y, text, on, delay = 0, color = C.mint}) => {
  const f = useCurrentFrame() - delay; const a = sp(f, 13, 180);
  return <div style={{position: 'absolute', left: x, top: y, transform: `scale(${a})`, opacity: Math.min(1, a * 1.5), padding: '14px 28px', borderRadius: 999, fontFamily: F, fontWeight: 700, fontSize: 32, whiteSpace: 'nowrap',
    background: on ? color : 'rgba(8,24,30,0.8)', color: on ? C.night0 : '#e6f4f1', border: `2px solid ${on ? color : 'rgba(127,240,214,0.35)'}`, boxShadow: on ? `0 0 40px ${color}66` : '0 14px 30px rgba(0,0,0,0.45)'}}>{text}</div>;
};

/* ================= CEK MUATAN ================= */
const MHook: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const s = 120;
  const cells = [] as {x: number; y: number; d: number; over: boolean}[];
  for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) cells.push({x: 300 + c * 125 - r * 20, y: 1040 - r * 125, d: (r * 4 + c) * 3, over: false});
  cells.push({x: 790, y: 790, d: 30, over: true}, {x: 860, y: 700, d: 36, over: true});
  return (
    <>
      <Head text="Barang naik, ternyata *tidak muat?*" top={260} size={96} />
      <div style={{position: 'absolute', left: 210, top: 820, width: 560, height: 320, border: `4px solid ${C.mint}`, borderRadius: 16, transform: 'perspective(1400px) rotateX(18deg) rotateY(-24deg)', boxShadow: `0 0 40px rgba(127,240,214,0.3), inset 0 0 40px rgba(127,240,214,0.15)`}} />
      {cells.map((c, i) => {
        const a = sp(f - c.d, 12, 150);
        const fall = c.over ? interpolate(f, [c.d + 22, c.d + 50], [0, 1], {...cl, easing: Easing.in(Easing.quad)}) : 0;
        return <Cube key={i} x={c.x + fall * 160} y={c.y - (1 - a) * 500 + fall * 700} s={s - 10} rx={-22} ry={-30 + fall * 120} o={a * (1 - fall * 0.4)} color={c.over ? C.orange : C.mint} label={c.over ? '!' : ''} />;
      })}
      {f > 40 && <Chip x={600} y={560} text="Kelebihan 2 unit" icon="!" color={C.red} delay={40} />}
    </>
  );
};

const MTipe: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame(); const a = sp(f, 16, 90);
  return (
    <>
      <Tag n="01" label="PILIH TIPE TRUK" />
      <Head text="Ukuran truk *tersimpan*" />
      <Phone src="iklan3d/m_type.png" x={640} y={1010} w={480} ry={-20 + (1 - a) * -40 + f * 0.08} rx={6} />
      <Pill x={50} y={620} text="CDD Bak" on delay={8} />
      <Pill x={50} y={720} text="Fuso Bak" delay={13} />
      <Pill x={50} y={820} text="Tronton Bak" delay={18} />
      <Pill x={50} y={920} text="+ Unit sendiri" delay={23} color={C.orange} />
      <Chip x={40} y={1220} text="450 × 200 × 200" sub="panjang × lebar × tinggi (cm)" icon="⬚" delay={28} />
    </>
  );
};

const MBarang: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame(); const a = sp(f, 16, 90);
  return (
    <>
      <Tag n="02" label="DATA BARANG" />
      <Head text="Isi ukuran & *berat*" />
      <Phone src="iklan3d/m_form.png" x={400} y={1010} w={480} ry={20 - f * 0.08 + (1 - a) * 40} rx={6} />
      <Chip x={560} y={640} text="Palet × 6" sub="120×100×110 cm · 450 kg" icon="1" delay={10} />
      <Chip x={600} y={880} text="Karton × 30" sub="60×40×50 cm · 20 kg" icon="2" delay={18} color={C.orange} />
      <Chip x={580} y={1120} text="Boleh ditumpuk" sub="atur per barang" icon="✓" delay={26} />
    </>
  );
};

const M3D: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const sw = interpolate(f, [dur * 0.45, dur * 0.6], [0, 1], {...cl, easing: eo});
  return (
    <>
      <Tag n="03" label="TAMPILAN 3D & 2D" />
      <Head text={sw < 0.5 ? 'Lihat susunan *3D*' : 'Atau dari atas, *2D*'} />
      <Phone src="iklan3d/m_3d.png" x={540 - sw * 230} y={1000} w={500 - sw * 120} ry={Math.sin(f / 25) * 14 + sw * 30} rx={6} o={1 - sw * 0.35} />
      <Phone src="iklan3d/m_2d.png" x={540 + (1 - sw) * 700 + sw * 230} y={1000} w={380 + sw * 120} ry={-30 + sw * 14} rx={6} o={sw} />
      <Pill x={110} y={1480} text="3D" on={sw < 0.5} delay={6} />
      <Pill x={250} y={1480} text="2D atas" on={sw >= 0.5} delay={10} />
      <Pill x={470} y={1480} text="2D samping" delay={14} />
    </>
  );
};

const MHasil: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame();
  return (
    <>
      <Tag n="04" label="HASIL" />
      <Head text="Muat, atau *sisa berapa*" />
      <Phone src="iklan3d/m_3d.png" x={290} y={1000} w={400} ry={22} rx={6} o={sp(f, 16, 100)} />
      <Phone src="iklan3d/m_nomuat.png" x={790} y={1000} w={400} ry={-22} rx={6} o={sp(f - 8, 16, 100)} />
      <Chip x={60} y={1330} text="Semua muat" sub="36 dari 36" icon="✓" delay={16} />
      <Chip x={560} y={1330} text="Sisa 4 unit" sub="Palet tidak muat" icon="!" delay={24} color={C.red} />
    </>
  );
};

const MBerat: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame();
  const g = interpolate(f, [8, 40], [0, 0.66], {...cl, easing: eo});
  const kg = Math.round(g / 0.66 * 3300);
  return (
    <>
      <Tag n="05" label="CEK BERAT" />
      <Head text="Berat *tidak lewat batas*" />
      <div style={{position: 'absolute', left: 120, right: 120, top: 640, padding: 50, borderRadius: 44, background: 'linear-gradient(170deg,rgba(255,255,255,0.08),rgba(255,255,255,0.02))', border: '2px solid rgba(127,240,214,0.3)', fontFamily: F,
        transform: `perspective(1600px) rotateX(${14 - sp(f) * 8}deg)`, boxShadow: '0 50px 100px rgba(0,0,0,0.55)'}}>
        <div style={{color: '#9fc4bf', fontSize: 34, fontWeight: 600}}>Berat total / maks CDD Bak</div>
        <div style={{color: '#fff', fontSize: 120, fontWeight: 800, letterSpacing: -3, marginTop: 10}}>{kg.toLocaleString('id-ID')}<span style={{fontSize: 56, color: '#9fc4bf'}}> / 5.000 kg</span></div>
        <div style={{height: 30, borderRadius: 30, background: 'rgba(255,255,255,0.1)', marginTop: 30, overflow: 'hidden'}}>
          <div style={{width: `${g * 100}%`, height: '100%', borderRadius: 30, background: `linear-gradient(90deg, ${C.mintDeep}, ${C.mint})`, boxShadow: `0 0 30px ${C.mint}`}} />
        </div>
      </div>
      <Chip x={170} y={1150} text="Aman, masih di bawah batas" icon="✓" delay={38} />
      <Chip x={220} y={1330} text="Lebih berat? Langsung ditandai" icon="!" delay={50} color={C.red} />
    </>
  );
};

/* ================= DATA TRUK ================= */
const Doc: React.FC<{x: number; y: number; title: string; date: string; r: number; delay: number}> = ({x, y, title, date, r, delay}) => {
  const f = useCurrentFrame() - delay; const a = sp(f, 13, 140); const st = sp(f - 18, 9, 220);
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 420, padding: '34px 36px', borderRadius: 30, background: C.cream, color: C.ink, fontFamily: F,
      transform: `perspective(1400px) rotateY(${r + (1 - a) * 70}deg) rotateZ(${r / 3}deg) scale(${a})`, boxShadow: '0 40px 80px rgba(0,0,0,0.55)'}}>
      <div style={{fontSize: 26, fontWeight: 600, color: '#6b7a7d', letterSpacing: 2}}>DOKUMEN</div>
      <div style={{fontSize: 52, fontWeight: 800, marginTop: 4}}>{title}</div>
      <div style={{fontSize: 30, color: '#5a6b70', marginTop: 10, marginBottom: 56}}>Berlaku s.d. {date}</div>
      <div style={{position: 'absolute', right: 24, bottom: 26, transform: `rotate(-12deg) scale(${1.8 - 0.8 * st})`, opacity: st, border: `5px solid ${C.red}`, color: C.red, fontWeight: 800, fontSize: 38, padding: '4px 16px', borderRadius: 10}}>LEWAT</div>
    </div>
  );
};

const THook: React.FC<{dur: number}> = () => (
  <>
    <Head text="STNK & KIR habis, *baru ketahuan?*" top={260} size={94} />
    <Doc x={90} y={640} title="STNK" date="12 Okt 2026" r={-16} delay={6} />
    <Doc x={560} y={820} title="KIR kepala" date="28 Okt 2026" r={14} delay={12} />
    <Doc x={200} y={1080} title="KIR buntut" date="1 Nov 2026" r={-6} delay={18} />
  </>
);

const TCatat: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame(); const a = sp(f, 16, 90);
  return (
    <>
      <Tag n="01" label="CATAT ARMADA" />
      <Head text="Semua armada *tercatat*" />
      <Phone src="iklan3d/t_list.png" x={660} y={1010} w={470} ry={-20 + (1 - a) * -40 + f * 0.08} rx={6} />
      <Chip x={40} y={640} text="B 9012 KLM" sub="Tronton · 2021" icon="🚚" delay={10} />
      <Chip x={30} y={860} text="L 8820 UX" sub="Fuso · 2021" icon="🚚" delay={16} color={C.orange} />
      <Chip x={50} y={1080} text="D 9133 FH" sub="Tronton · 2021" icon="🚚" delay={22} />
    </>
  );
};

const TDok: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame(); const a = sp(f, 16, 90);
  return (
    <>
      <Tag n="02" label="DOKUMEN & FOTO" />
      <Head text="STNK & KIR, *plus foto*" />
      <Phone src="iklan3d/t_edit.png" x={400} y={1010} w={470} ry={20 - f * 0.08 + (1 - a) * 40} rx={6} />
      <Chip x={580} y={620} text="STNK" sub="s.d. 1 Mei 2027" icon="✓" delay={10} />
      <Chip x={600} y={840} text="KIR kepala" sub="sisa 6 hari" icon="!" delay={16} color={C.orange} />
      <Chip x={590} y={1060} text="KIR buntut" sub="s.d. 1 Feb 2027" icon="✓" delay={22} />
      <Chip x={560} y={1280} text="Foto dokumen" sub="tersimpan di HP" icon="📷" delay={28} />
    </>
  );
};

const Stat3D: React.FC<{x: number; y: number; label: string; val: string; color: string; delay: number}> = ({x, y, label, val, color, delay}) => {
  const f = useCurrentFrame() - delay; const a = sp(f, 12, 150); const bob = Math.sin((f + delay) / 15) * 10;
  return (
    <div style={{position: 'absolute', left: x, top: y + bob, width: 400, height: 260, borderRadius: 40, padding: '36px 40px', fontFamily: F,
      background: 'linear-gradient(160deg, rgba(255,255,255,0.12), rgba(255,255,255,0.03))', border: `3px solid ${color}88`,
      transform: `perspective(1400px) rotateX(14deg) rotateY(${(x < 500 ? 16 : -16)}deg) scale(${a})`, boxShadow: `0 40px 80px rgba(0,0,0,0.5), 0 0 50px ${color}33`}}>
      <div style={{color: '#b6d2cd', fontSize: 34, fontWeight: 600}}>{label}</div>
      <div style={{color, fontSize: 130, fontWeight: 800, lineHeight: 1, marginTop: 10, textShadow: `0 0 40px ${color}66`}}>{val}</div>
    </div>
  );
};

const TRingkas: React.FC<{dur: number}> = () => (
  <>
    <Tag n="03" label="RINGKASAN" />
    <Head text="Status *sekilas pandang*" />
    <Stat3D x={90} y={620} label="Truk" val="4" color="#ffffff" delay={6} />
    <Stat3D x={590} y={620} label="≤ 30 hari" val="2" color={C.orange} delay={12} />
    <Stat3D x={90} y={940} label="Sudah lewat" val="1" color={C.red} delay={18} />
    <Stat3D x={590} y={940} label="Belum lengkap" val="0" color={C.mint} delay={24} />
    <Chip x={170} y={1300} text="Perlu diperpanjang: 3 dokumen" icon="!" delay={32} color={C.orange} />
  </>
);

const TFilter: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame(); const a = sp(f, 16, 90);
  const q = 'B 9012'; const n = Math.max(0, Math.min(q.length, Math.floor((f - 30) / 3)));
  return (
    <>
      <Tag n="04" label="FILTER & CARI" />
      <Head text="Filter per *dokumen*" />
      <Phone src="iklan3d/t_filter.png" x={660} y={1040} w={440} ry={-20 + (1 - a) * -40} rx={6} />
      <Pill x={40} y={640} text="Semua dok." delay={6} />
      <Pill x={40} y={740} text="STNK" delay={10} />
      <Pill x={40} y={840} text="KIR kepala" on delay={14} />
      <Pill x={40} y={940} text="KIR buntut" delay={18} />
      <div style={{position: 'absolute', left: 40, top: 1120, width: 420, padding: '22px 28px', borderRadius: 26, background: 'rgba(8,24,30,0.85)', border: `2px solid ${C.mint}`, fontFamily: F, fontSize: 38, color: '#fff', opacity: sp(f - 24), boxShadow: '0 20px 50px rgba(0,0,0,0.5)'}}>
        <span style={{color: C.mint, marginRight: 14}}>⌕</span>{q.slice(0, n)}<span style={{opacity: f % 20 < 10 ? 1 : 0, color: C.mint}}>|</span>
      </div>
    </>
  );
};

const TNotif: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame(); const a = sp(f, 16, 90);
  const ring = Math.sin(f / 2.2) * interpolate(f % 45, [0, 20], [16, 0], cl);
  return (
    <>
      <Tag n="05" label="PERINGATAN" />
      <Head text="Diingatkan *sebelum habis*" />
      <Phone src="iklan3d/t_notif.png" x={660} y={1040} w={440} ry={-20 + (1 - a) * -40} rx={6} />
      <div style={{position: 'absolute', left: 90, top: 640, width: 260, height: 260, borderRadius: 70, background: 'linear-gradient(160deg,#16413f,#0a1f22)', border: `3px solid ${C.mint}`, display: 'grid', placeItems: 'center',
        transform: `perspective(1200px) rotateY(18deg) rotateZ(${ring}deg) scale(${sp(f - 4)})`, boxShadow: `0 40px 80px rgba(0,0,0,0.5), 0 0 60px rgba(127,240,214,0.35)`}}>
        <svg width="140" height="140" viewBox="0 0 24 24" fill="none" stroke={C.mint} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
        <div style={{position: 'absolute', right: 18, top: 18, width: 64, height: 64, borderRadius: '50%', background: C.red, color: '#fff', fontFamily: F, fontWeight: 800, fontSize: 38, display: 'grid', placeItems: 'center'}}>3</div>
      </div>
      <Chip x={40} y={1000} text="Sebulan lagi" sub="pengingat pertama" icon="1" delay={16} color={C.orange} />
      <Chip x={40} y={1200} text="Seminggu lagi" sub="pengingat kedua" icon="!" delay={24} color={C.red} />
    </>
  );
};

const MAP: Record<string, React.FC<{dur: number}>> = {
  mhook: MHook, mtipe: MTipe, mbarang: MBarang, m3d: M3D, mhasil: MHasil, mberat: MBerat,
  thook: THook, tcatat: TCatat, tdok: TDok, tringkas: TRingkas, tfilter: TFilter, tnotif: TNotif,
  logo: S1Logo, cta: S8CTA,
};

export const IklanFokus: React.FC<IklanProps> = ({scenes}) => {
  useOutfit();
  return (
    <AbsoluteFill style={{background: C.night0}}>
      <Stage />
      {scenes.map((s, i) => {
        const Comp = MAP[s.key];
        return (
          <Sequence key={i} from={s.from} durationInFrames={s.dur}>
            <Trans dur={s.dur} last={i === scenes.length - 1}><Comp dur={s.dur} /></Trans>
            {s.sub && <Sub text={s.sub} dur={s.dur} />}
          </Sequence>
        );
      })}
      <div style={{position: 'absolute', left: 50, top: 62, display: 'flex', alignItems: 'center', gap: 12, fontFamily: F, fontWeight: 700, fontSize: 28, color: '#cfe8e3'}}>
        <Img src={staticFile('icon.png')} style={{width: 48, height: 48, borderRadius: 12}} />Ghostrip
      </div>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 60%, rgba(0,0,0,0.5) 100%)', pointerEvents: 'none'}} />
    </AbsoluteFill>
  );
};
