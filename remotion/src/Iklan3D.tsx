// Iklan fitur Ghostrip gaya "3D startup tech" (sekali pakai, di luar jadwal konten harian).
import React, {useState} from 'react';
import {
  AbsoluteFill, Img, Sequence, continueRender, delayRender, interpolate, spring, staticFile,
  useCurrentFrame, useVideoConfig, Easing,
} from 'remotion';
import {C} from './theme';

const cl = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const eo = Easing.bezier(0.16, 1, 0.3, 1);
const F = 'Outfit';

export type IklanScene = {key: string; from: number; dur: number; sub: string};
export type IklanProps = {scenes: IklanScene[]; durationInFrames: number};

const useOutfit = () => {
  const [h] = useState(() => delayRender('font'));
  React.useEffect(() => {
    const f = new FontFace('Outfit', `url(${staticFile('Outfit.ttf')})`, {weight: '100 900'});
    f.load().then((ff) => { (document.fonts as any).add(ff); continueRender(h); });
  }, [h]);
};

const sp = (f: number, d = 16, s = 140) => spring({frame: f, fps: 30, config: {damping: d, stiffness: s}});

/* ---------- latar: lantai grid perspektif + cahaya + partikel ---------- */
const Stage: React.FC = () => {
  const f = useCurrentFrame();
  const off = (f * 3) % 120;
  return (
    <AbsoluteFill style={{background: `radial-gradient(1200px 900px at 50% 38%, #0d3a44 0%, ${C.night1} 45%, ${C.night0} 80%)`, overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: -1200, right: -1200, top: 1180, height: 1600, perspective: 900}}>
        <div style={{position: 'absolute', inset: 0, transform: 'rotateX(74deg)', transformOrigin: '50% 0%',
          backgroundImage: `linear-gradient(rgba(127,240,214,0.22) 2px, transparent 2px), linear-gradient(90deg, rgba(127,240,214,0.22) 2px, transparent 2px)`,
          backgroundSize: '120px 120px', backgroundPosition: `0 ${off}px`,
          maskImage: 'linear-gradient(to bottom, rgba(0,0,0,0.9), transparent 75%)', WebkitMaskImage: 'linear-gradient(to bottom, rgba(0,0,0,0.9), transparent 75%)'}} />
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1150, height: 4, background: `linear-gradient(90deg, transparent, ${C.mint}, transparent)`, opacity: 0.55, filter: 'blur(1px)'}} />
      <div style={{position: 'absolute', left: 140, top: 260, width: 520, height: 520, borderRadius: '50%', background: 'rgba(47,184,160,0.18)', filter: 'blur(120px)'}} />
      <div style={{position: 'absolute', right: 60, top: 900, width: 460, height: 460, borderRadius: '50%', background: 'rgba(255,157,92,0.10)', filter: 'blur(130px)'}} />
      {Array.from({length: 26}).map((_, i) => {
        const x = (i * 397) % 1080, y0 = (i * 733) % 1900;
        const y = (y0 - f * (0.6 + (i % 5) * 0.25) + 3800) % 1900;
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: 4 + (i % 3) * 2, height: 4 + (i % 3) * 2, borderRadius: '50%', background: C.mint, opacity: 0.18 + (i % 4) * 0.08, boxShadow: `0 0 12px ${C.mint}`}} />;
      })}
    </AbsoluteFill>
  );
};

/* ---------- HP 3D ---------- */
const Phone: React.FC<{src: string; x: number; y: number; w?: number; ry?: number; rx?: number; rz?: number; s?: number; o?: number; glow?: boolean}> = ({src, x, y, w = 560, ry = 0, rx = 0, rz = 0, s = 1, o = 1, glow = true}) => {
  const h = w * 2.164;
  return (
    <div style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, perspective: 2200, opacity: o}}>
      <div style={{width: '100%', height: '100%', transform: `scale(${s}) rotateX(${rx}deg) rotateY(${ry}deg) rotateZ(${rz}deg)`, transformStyle: 'preserve-3d'}}>
        {glow && <div style={{position: 'absolute', inset: -40, borderRadius: 110, background: 'rgba(127,240,214,0.25)', filter: 'blur(60px)', transform: 'translateZ(-60px)'}} />}
        <div style={{position: 'absolute', inset: 0, borderRadius: w * 0.14, background: 'linear-gradient(145deg,#2a3f47,#0b161b 55%,#22343b)', padding: w * 0.032,
          boxShadow: `0 60px 120px rgba(0,0,0,0.65), inset 0 0 0 3px rgba(255,255,255,0.08), 0 0 0 2px rgba(127,240,214,0.25)`}}>
          <div style={{width: '100%', height: '100%', borderRadius: w * 0.11, overflow: 'hidden', position: 'relative', background: '#fff'}}>
            <Img src={staticFile(src)} style={{width: '100%', display: 'block'}} />
            <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(115deg, rgba(255,255,255,0.22) 0%, rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,0.08) 100%)'}} />
          </div>
        </div>
      </div>
    </div>
  );
};

/* ---------- tipografi ---------- */
const Head: React.FC<{text: string; top?: number; size?: number; delay?: number}> = ({text, top = 210, size = 92, delay = 0}) => {
  const f = useCurrentFrame() - delay;
  const words = text.split(' ');
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top, textAlign: 'center', fontFamily: F, fontWeight: 800, fontSize: size, lineHeight: 1.04, letterSpacing: -2.5, color: '#fff'}}>
      {words.map((w, i) => {
        const a = sp(f - i * 3, 15, 170);
        const hi = w.startsWith('*');
        const t = w.replace(/\*/g, '');
        return <span key={i} style={{display: 'inline-block', marginRight: '0.24em', opacity: a, transform: `translateY(${(1 - a) * 50}px) rotateX(${(1 - a) * 70}deg)`, color: hi ? C.mint : '#fff', textShadow: hi ? `0 0 30px rgba(127,240,214,0.55)` : '0 6px 30px rgba(0,0,0,0.5)'}}>{t}</span>;
      })}
    </div>
  );
};

const Tag: React.FC<{n: string; label: string; delay?: number; top?: number}> = ({n, label, delay = 0, top = 130}) => {
  const f = useCurrentFrame() - delay;
  const a = sp(f, 18, 160);
  return (
    <div style={{position: 'absolute', top, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: a, transform: `translateY(${(1 - a) * -20}px)`}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 14, padding: '10px 24px 10px 12px', borderRadius: 999, background: 'rgba(127,240,214,0.10)', border: '2px solid rgba(127,240,214,0.45)', fontFamily: F, fontWeight: 700, fontSize: 30, color: C.mint, letterSpacing: 3}}>
        <span style={{background: C.mint, color: C.night0, borderRadius: 999, padding: '2px 14px', fontSize: 26}}>{n}</span>{label}
      </div>
    </div>
  );
};

const Chip: React.FC<{x: number; y: number; text: string; sub?: string; delay?: number; color?: string; icon?: string}> = ({x, y, text, sub, delay = 0, color = C.mint, icon}) => {
  const f = useCurrentFrame() - delay;
  const a = sp(f, 13, 180);
  const bob = Math.sin((f + delay) / 14) * 8;
  return (
    <div style={{position: 'absolute', left: x, top: y + bob, transform: `scale(${a}) translateZ(0)`, opacity: Math.min(1, a * 1.4), transformOrigin: 'center',
      background: 'rgba(8,24,30,0.72)', backdropFilter: 'blur(14px)', border: `2px solid ${color}55`, borderRadius: 26, padding: '18px 26px', fontFamily: F,
      boxShadow: `0 20px 50px rgba(0,0,0,0.5), 0 0 30px ${color}33`, display: 'flex', alignItems: 'center', gap: 16}}>
      {icon && <span style={{width: 56, height: 56, borderRadius: 16, background: `${color}22`, color, display: 'grid', placeItems: 'center', fontSize: 32, fontWeight: 800}}>{icon}</span>}
      <div>
        <div style={{color: '#fff', fontWeight: 800, fontSize: 38, letterSpacing: -0.5, whiteSpace: 'nowrap'}}>{text}</div>
        {sub && <div style={{color: '#9fc4bf', fontWeight: 500, fontSize: 24, marginTop: 2, whiteSpace: 'nowrap'}}>{sub}</div>}
      </div>
    </div>
  );
};

const Sub: React.FC<{text: string; dur: number}> = ({text, dur}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 6, dur - 6, dur], [0, 1, 1, 0], cl);
  return (
    <div style={{position: 'absolute', left: 80, right: 80, top: 1590, textAlign: 'center', opacity: o}}>
      <span style={{fontFamily: F, fontWeight: 600, fontSize: 40, lineHeight: 1.3, color: '#eafaf6', background: 'rgba(4,13,19,0.62)', padding: '8px 20px', borderRadius: 14, boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone'}}>{text}</span>
    </div>
  );
};

const Simulasi: React.FC = () => (
  <div style={{position: 'absolute', right: 50, top: 60, fontFamily: F, fontWeight: 700, fontSize: 22, letterSpacing: 3, color: C.orange, border: `2px solid ${C.orange}88`, borderRadius: 999, padding: '6px 16px'}}>DATA SIMULASI</div>
);

/* ---------- kubus 3D (untuk cek muatan & hook) ---------- */
const Cube: React.FC<{x: number; y: number; s: number; rx: number; ry: number; color?: string; label?: string; o?: number}> = ({x, y, s, rx, ry, color = C.mint, label, o = 1}) => {
  const face = (t: string, shade: number) => (
    <div style={{position: 'absolute', width: s, height: s, transform: t, background: `rgba(${color === C.mint ? '127,240,214' : '255,157,92'},${0.16 + shade})`, border: `2px solid ${color}`, boxShadow: `inset 0 0 30px ${color}55`, display: 'grid', placeItems: 'center', color: '#fff', fontFamily: F, fontWeight: 800, fontSize: s * 0.18, backfaceVisibility: 'visible'}}>{label}</div>
  );
  return (
    <div style={{position: 'absolute', left: x - s / 2, top: y - s / 2, width: s, height: s, perspective: 1600, opacity: o}}>
      <div style={{width: s, height: s, position: 'relative', transformStyle: 'preserve-3d', transform: `rotateX(${rx}deg) rotateY(${ry}deg)`}}>
        {face(`translateZ(${s / 2}px)`, 0.12)}
        {face(`rotateY(180deg) translateZ(${s / 2}px)`, 0)}
        {face(`rotateY(90deg) translateZ(${s / 2}px)`, 0.05)}
        {face(`rotateY(-90deg) translateZ(${s / 2}px)`, 0.05)}
        {face(`rotateX(90deg) translateZ(${s / 2}px)`, 0.2)}
        {face(`rotateX(-90deg) translateZ(${s / 2}px)`, 0)}
      </div>
    </div>
  );
};

/* ================= ADEGAN ================= */
const S0Hook: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const items = [['Kalkulator', 240, 820, -14], ['Excel', 760, 760, 10], ['Ketik ulang', 520, 1060, -4]] as const;
  return (
    <>
      <Head text="Hitung trip masih *manual?*" top={300} size={104} />
      {items.map(([t, x, y, r], i) => {
        const a = sp(f - 8 - i * 6, 12, 150);
        const strike = interpolate(f, [34 + i * 6, 46 + i * 6], [0, 1], {...cl, easing: eo});
        const fall = interpolate(f, [dur - 18, dur], [0, 1], {...cl, easing: Easing.in(Easing.cubic)});
        return (
          <div key={t} style={{position: 'absolute', left: x, top: y + fall * 900, transform: `translate(-50%,-50%) perspective(1200px) rotateX(${18 - fall * 60}deg) rotateY(${r * 2}deg) rotateZ(${r + fall * r * 3}deg) scale(${a})`,
            padding: '34px 50px', borderRadius: 32, background: 'linear-gradient(160deg, rgba(255,255,255,0.14), rgba(255,255,255,0.03))', border: '2px solid rgba(255,255,255,0.18)', backdropFilter: 'blur(10px)',
            fontFamily: F, fontWeight: 800, fontSize: 64, color: '#dfeeee', boxShadow: '0 40px 80px rgba(0,0,0,0.5)'}}>
            <span style={{position: 'relative'}}>{t}
              <span style={{position: 'absolute', left: -10, right: -10, top: '52%', height: 9, borderRadius: 9, background: C.red, transform: `scaleX(${strike})`, transformOrigin: 'left', boxShadow: `0 0 18px ${C.red}`}} />
            </span>
          </div>
        );
      })}
    </>
  );
};

const S1Logo: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame();
  const a = sp(f, 11, 120);
  const ring = interpolate(f, [0, 40], [0.3, 1.6], {...cl, easing: eo});
  const ro = interpolate(f, [0, 40], [0.9, 0], cl);
  return (
    <>
      <div style={{position: 'absolute', left: 540 - 300, top: 800 - 300, width: 600, height: 600, borderRadius: '50%', border: `4px solid ${C.mint}`, transform: `scale(${ring})`, opacity: ro}} />
      <div style={{position: 'absolute', left: 540 - 190, top: 800 - 190, width: 380, height: 380, perspective: 1400}}>
        <Img src={staticFile('icon.png')} style={{width: 380, height: 380, borderRadius: 90, transform: `rotateY(${(1 - a) * 180}deg) rotateX(${Math.sin(f / 18) * 8}deg) scale(${0.6 + 0.4 * a})`,
          boxShadow: `0 50px 120px rgba(0,0,0,0.6), 0 0 120px rgba(127,240,214,${0.35 * a})`}} />
      </div>
      <div style={{position: 'absolute', top: 1060, left: 0, right: 0, textAlign: 'center', fontFamily: F, fontWeight: 800, fontSize: 150, letterSpacing: -5, color: '#fff', opacity: sp(f - 8), transform: `translateY(${(1 - sp(f - 8)) * 40}px)`}}>
        Ghost<span style={{color: C.mint}}>rip</span>
      </div>
      <div style={{position: 'absolute', top: 1250, left: 0, right: 0, textAlign: 'center', fontFamily: F, fontWeight: 500, fontSize: 40, letterSpacing: 6, color: '#9fc4bf', opacity: sp(f - 16)}}>APLIKASI EKSPEDISI TRUK</div>
    </>
  );
};

const S2Hitung: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const a = sp(f, 16, 90);
  return (
    <>
      <Tag n="01" label="HITUNG TRIP" />
      <Head text="Harga trip *otomatis*" />
      <Phone src="iklan3d/hasil.png" x={560 + (1 - a) * 500} y={1020} w={540} ry={-22 + (1 - a) * -40 + f * 0.12} rx={6} />
      <Chip x={60} y={620} text="780 km" sub="Jakarta → Surabaya" icon="↗" delay={10} />
      <Chip x={40} y={900} text="3 hari" sub="jalan + istirahat" icon="⏱" delay={16} color={C.orange} />
      <Chip x={90} y={1180} text="Solar + tol" sub="dihitung sekaligus" icon="⛽" delay={22} />
      <Simulasi />
    </>
  );
};

const S3Surat: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame();
  const a = sp(f, 16, 90);
  const out = sp(f - 14, 14, 70);
  return (
    <>
      <Tag n="02" label="SURAT PENAWARAN" />
      <Head text="PDF siap kirim, *rapi*" />
      <Phone src="iklan3d/surat.png" x={330} y={1040} w={420} ry={28 - f * 0.08} rx={4} o={a} />
      <div style={{position: 'absolute', left: 430, top: 470, width: 560, perspective: 1800}}>
        <Img src={staticFile('iklan3d/sheet.png')} style={{width: 560, borderRadius: 10, transform: `translateX(${(1 - out) * -240}px) translateY(${(1 - out) * 200}px) rotateY(${-24 + (1 - out) * 40}deg) rotateX(${8}deg) rotateZ(${3 - out * 3}deg) scale(${0.5 + 0.5 * out})`,
          opacity: out, boxShadow: '0 60px 120px rgba(0,0,0,0.6), 0 0 60px rgba(127,240,214,0.25)'}} />
      </div>
      {['Kop surat', 'TTD & cap', 'PPN / PPh'].map((t, i) => <Chip key={t} x={560 + (i % 2) * 40} y={1260 + i * 104} text={t} icon="✓" delay={28 + i * 6} />)}
    </>
  );
};

const S4WA: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame();
  const a = sp(f, 15, 120);
  const fly = sp(f - 10, 14, 90);
  const read = f > 40;
  return (
    <>
      <Tag n="03" label="KIRIM KE WHATSAPP" />
      <Head text="Satu ketuk, *terkirim*" />
      <div style={{position: 'absolute', left: 120, right: 120, top: 600, height: 620, borderRadius: 50, background: 'linear-gradient(170deg,#0f2a30,#08161b)', border: '2px solid rgba(127,240,214,0.25)', transform: `perspective(1600px) rotateX(${12 - a * 6}deg) scale(${0.85 + 0.15 * a})`, opacity: a, boxShadow: '0 60px 120px rgba(0,0,0,0.6)', overflow: 'hidden'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 20, padding: '30px 36px', background: 'rgba(255,255,255,0.04)', fontFamily: F}}>
          <div style={{width: 74, height: 74, borderRadius: '50%', background: '#2c4a50', display: 'grid', placeItems: 'center', color: C.mint, fontWeight: 800, fontSize: 30}}>PM</div>
          <div><div style={{color: '#fff', fontWeight: 700, fontSize: 34}}>PT Makmur Semakmurnya</div><div style={{color: '#8fb1ac', fontSize: 24}}>online</div></div>
        </div>
        <div style={{position: 'absolute', left: 40, top: 170, maxWidth: 560, background: '#1c3238', color: '#eafaf6', fontFamily: F, fontSize: 32, padding: '18px 26px', borderRadius: '8px 28px 28px 28px'}}>Pak, minta harga Jakarta–Surabaya ya 🙏</div>
        <div style={{position: 'absolute', right: 40, top: 330, width: 520, transform: `translateY(${(1 - fly) * 500}px) scale(${0.6 + 0.4 * fly})`, opacity: fly, background: '#14574d', borderRadius: '28px 8px 28px 28px', padding: 18, fontFamily: F}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 18, background: 'rgba(0,0,0,0.22)', borderRadius: 18, padding: 18}}>
            <div style={{width: 70, height: 84, borderRadius: 10, background: C.red, color: '#fff', display: 'grid', placeItems: 'center', fontWeight: 800, fontSize: 24}}>PDF</div>
            <div><div style={{color: '#fff', fontWeight: 700, fontSize: 30}}>Surat_Penawaran.pdf</div><div style={{color: '#b9e3da', fontSize: 24}}>1 halaman · PDF</div></div>
          </div>
          <div style={{textAlign: 'right', color: read ? '#7fd8ff' : '#b9e3da', fontSize: 28, marginTop: 8, fontWeight: 700}}>✓✓</div>
        </div>
      </div>
    </>
  );
};

const S5Muat: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame();
  const a = sp(f, 16, 90);
  const cubes = [[150, 650], [290, 560], [130, 860], [930, 720], [960, 980], [820, 540]];
  return (
    <>
      <Tag n="04" label="CEK MUATAN 3D" />
      <Head text="Muat atau tidak? *Kelihatan*" />
      <Phone src="iklan3d/muat_top.png" x={540} y={1000} w={460} ry={Math.sin(f / 30) * 16} rx={8} s={0.8 + 0.2 * a} />
      {cubes.map(([x, y], i) => {
        const c = sp(f - 6 - i * 4, 12, 140);
        return <Cube key={i} x={x} y={y} s={90 + (i % 3) * 24} rx={-24 + Math.sin(f / 20 + i) * 10} ry={f * 1.6 + i * 40} o={c} color={i % 3 === 1 ? C.orange : C.mint} />;
      })}
      <Chip x={300} y={1330} text="Semua barang muat" sub="6 dari 6 palet · 1.800 kg" icon="✓" delay={24} />
    </>
  );
};

const S6Semua: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame();
  const a = sp(f, 16, 80);
  const tiles = [['Data truk', '🚚'], ['STNK & KIR', '📄'], ['Berita logistik', '📰'], ['Warna surat', '🎨'], ['Riwayat', '🕘'], ['Quotation', '🧾']];
  return (
    <>
      <Tag n="05" label="SEMUA DI SATU APLIKASI" />
      <Head text="Satu aplikasi, *lengkap*" />
      <Phone src="iklan3d/armada.png" x={250} y={940} w={360} ry={30} rx={6} o={a} s={0.9} glow={false} />
      <Phone src="iklan3d/home.png" x={540} y={900} w={430} ry={Math.sin(f / 26) * 6} rx={4} s={0.8 + 0.2 * a} />
      <Phone src="iklan3d/warna.png" x={830} y={940} w={360} ry={-30} rx={6} o={a} s={0.9} glow={false} />
      {tiles.map(([t, ic], i) => {
        const ang = (i / tiles.length) * Math.PI * 2 + f / 40;
        const x = 540 + Math.cos(ang) * 330 - 140, y = 1420 + Math.sin(ang) * 55;
        const c = sp(f - 10 - i * 4, 14, 150);
        return (
          <div key={t} style={{position: 'absolute', left: x, top: y, width: 280, whiteSpace: 'nowrap', fontSize: 28, transform: `scale(${c * (0.82 + 0.18 * (Math.sin(ang) + 1) / 2)})`, zIndex: Math.round(Math.sin(ang) * 10) + 10,
            display: 'flex', alignItems: 'center', gap: 12, background: 'rgba(8,24,30,0.82)', border: '2px solid rgba(127,240,214,0.4)', borderRadius: 22, padding: '14px 18px', fontFamily: F, fontWeight: 700, color: '#fff', boxShadow: '0 20px 40px rgba(0,0,0,0.5)'}}>
            <span style={{fontSize: 34}}>{ic}</span>{t}
          </div>
        );
      })}
    </>
  );
};

const S7Akun: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame();
  const a = sp(f, 16, 100);
  const p = (f % 45) / 45;
  return (
    <>
      <Tag n="06" label="TERSIMPAN DI AKUN" />
      <Head text="Ganti HP, data *tetap aman*" />
      <Phone src="iklan3d/home.png" x={300} y={1040} w={380} ry={24} rx={6} o={a} />
      <Phone src="iklan3d/home.png" x={790} y={1040} w={380} ry={-24} rx={6} o={sp(f - 10, 16, 100)} />
      <div style={{position: 'absolute', left: 430, top: 590, width: 220, height: 150, borderRadius: 80, background: 'rgba(127,240,214,0.12)', border: `3px solid ${C.mint}`, display: 'grid', placeItems: 'center', fontFamily: F, fontWeight: 800, fontSize: 30, color: C.mint, boxShadow: `0 0 60px rgba(127,240,214,0.35)`, transform: `scale(${sp(f - 6)})`}}>AKUN</div>
      {[0, 1].map((k) => (
        <div key={k} style={{position: 'absolute', left: k ? 650 + p * 120 : 430 - p * 120, top: 740 + p * 140, width: 26, height: 26, borderRadius: '50%', background: C.mint, boxShadow: `0 0 24px ${C.mint}`, opacity: 1 - p}} />
      ))}
    </>
  );
};

const S8CTA: React.FC<{dur: number}> = () => {
  const f = useCurrentFrame();
  const a = sp(f, 13, 130);
  const pulse = 1 + Math.sin(f / 6) * 0.025;
  return (
    <>
      <Img src={staticFile('icon.png')} style={{position: 'absolute', left: 540 - 130, top: 380, width: 260, height: 260, borderRadius: 64, transform: `scale(${a}) rotateY(${Math.sin(f / 20) * 12}deg)`, boxShadow: '0 40px 100px rgba(0,0,0,0.55), 0 0 90px rgba(127,240,214,0.35)'}} />
      <Head text="Coba *gratis* 7 hari" top={740} size={100} delay={4} />
      <div style={{position: 'absolute', top: 1010, left: 0, right: 0, textAlign: 'center', fontFamily: F, fontWeight: 500, fontSize: 40, color: '#9fc4bf', opacity: sp(f - 12)}}>Langganan mulai Rp219.000/bulan</div>
      <div style={{position: 'absolute', top: 1140, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: sp(f - 16)}}>
        <div style={{transform: `scale(${pulse * sp(f - 16)})`, display: 'flex', alignItems: 'center', gap: 22, background: C.mint, color: C.night0, fontFamily: F, fontWeight: 800, fontSize: 52, padding: '30px 56px', borderRadius: 999, boxShadow: '0 30px 80px rgba(127,240,214,0.45)'}}>
          <span style={{width: 70, height: 70, borderRadius: '50%', background: C.night0, color: C.mint, display: 'grid', placeItems: 'center', fontSize: 38}}>✆</span>
          0815-1704-7930
        </div>
      </div>
      <div style={{position: 'absolute', top: 1330, left: 0, right: 0, textAlign: 'center', fontFamily: F, fontWeight: 700, fontSize: 40, letterSpacing: 2, color: '#fff', opacity: sp(f - 22)}}>Chat WhatsApp · ghostrip.id</div>
    </>
  );
};

const MAP: Record<string, React.FC<{dur: number}>> = {hook: S0Hook, logo: S1Logo, hitung: S2Hitung, surat: S3Surat, wa: S4WA, muat: S5Muat, semua: S6Semua, akun: S7Akun, cta: S8CTA};

const Trans: React.FC<{dur: number; children: React.ReactNode; last: boolean}> = ({dur, children, last}) => {
  const f = useCurrentFrame();
  const i = interpolate(f, [0, 8], [0, 1], {...cl, easing: eo});
  const o = last ? 1 : interpolate(f, [dur - 6, dur], [1, 0], cl);
  const z = interpolate(f, [0, dur], [1, 1.04], cl);
  return <AbsoluteFill style={{opacity: Math.min(i, o), transform: `scale(${z * (0.96 + 0.04 * i)})`, filter: `blur(${(1 - i) * 8}px)`}}>{children}</AbsoluteFill>;
};

export const Iklan3D: React.FC<IklanProps> = ({scenes}) => {
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
