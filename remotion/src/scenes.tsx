import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, random} from 'remotion';
import {C, W, H, SceneSpec} from './theme';
import {Bokeh, Camera, Lamp, NightSky, Paper, Person, Truck, clamp, easeOut} from './parts';

export const rp = (n: number) => (n < 0 ? '-' : '') + 'Rp' + Math.round(Math.abs(n)).toLocaleString('id-ID');
const num = (n: number, d = 0) => n.toLocaleString('id-ID', {minimumFractionDigits: d, maximumFractionDigits: d});

// hitung naik/turun dengan easing, dimulai sedikit setelah adegan muncul
const useCount = (from: number, to: number, dur: number, start = 6, frac = 0.6) => {
  const f = useCurrentFrame();
  return interpolate(f, [start, start + dur * frac], [from, to], {...clamp, easing: easeOut});
};

/* ---------- 1. JALAN: truk datang ke lokasi (jembatan timbang / tol / SPBU / gudang / pool) ---------- */
export const Jalan: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const arrive = spring({frame: f, fps, config: {damping: 200, stiffness: 18, mass: 1}});
  const tx = interpolate(arrive, [0, 1], [-900, s.stopX ?? 60]);
  const speed = interpolate(arrive, [0, 0.95, 1], [1, 0.25, 0], clamp);
  const sign = s.papan ?? 'JEMBATAN TIMBANG';
  return (
    <Camera dur={s.dur} to={1.08} oy="62%">
      <NightSky horizon={1180} />
      {/* bangunan & kanopi berlampu (seperti kanopi SPBU di referensi) */}
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <defs>
          <linearGradient id="road" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#1d3138" /><stop offset="1" stopColor="#0b161b" /></linearGradient>
          <linearGradient id="canopy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#d9dfdc" /><stop offset="1" stopColor="#9fb0ae" /></linearGradient>
        </defs>
        <path d="M0 1180 L1080 1180 L1080 1920 L0 1920 Z" fill="url(#road)" />
        <rect x={0} y={1600} width={W} height={10} fill="#2a4148" />
        {Array.from({length: 7}).map((_, i) => <rect key={i} x={i * 180 - 40} y={1720} width={110} height={10} rx={5} fill="#d9c27a" opacity={0.5} />)}
        {/* platform timbang bergaris kuning-hitam */}
        <rect x={40} y={1585} width={1000} height={22} fill="#2b3a3f" />
        {Array.from({length: 25}).map((_, i) => <rect key={i} x={40 + i * 40} y={1585} width={20} height={22} fill="#e8c44a" opacity={0.75} />)}
        {/* pos jaga dengan jendela menyala */}
        <rect x={720} y={1030} width={300} height={260} fill="#14262d" />
        <rect x={750} y={1080} width={240} height={110} fill="#ffd9a0" opacity={0.9} />
        <rect x={750} y={1080} width={240} height={110} fill="url(#canopy)" opacity={0.12} />
        <rect x={700} y={1010} width={340} height={26} fill="#0f1d23" />
        {/* kanopi */}
        <polygon points="-40,820 1120,820 1080,880 0,880" fill="url(#canopy)" />
        <rect x={-40} y={880} width={1160} height={26} fill="#5f7472" />
        {[120, 360, 600, 840].map((x, i) => (
          <g key={i}>
            <rect x={x} y={830} width={140} height={20} rx={6} fill="#fff7e2" />
            <ellipse cx={x + 70} cy={1000} rx={170} ry={260} fill="rgba(255,240,205,0.07)" />
          </g>
        ))}
        {[60, 1000].map((x) => <rect key={x} x={x} y={906} width={28} height={700} fill="#4b5f62" />)}
        {/* papan nama */}
        <rect x={250} y={740} width={580} height={86} rx={8} fill={C.teal} stroke={C.mint} strokeWidth={4} />
        <text x={540} y={798} textAnchor="middle" fontFamily="Outfit" fontWeight={800} fontSize={46} fill="#eafffa" letterSpacing={4}>{sign}</text>
      </svg>
      <Lamp x={940} y={700} h={600} s={0.9} />
      <Truck x={tx} y={1255} s={0.95} speed={speed} label={s.muatanLabel ?? ''} />
    </Camera>
  );
};

/* ---------- 2. DOKUMEN: kartu surat jalan dengan baris yang disorot ---------- */
export const Dokumen: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame: f, fps, config: {damping: 14, stiffness: 120}});
  const rows: [string, string][] = s.baris ?? [];
  const hi = s.sorot ?? rows.length - 1;
  const circle = interpolate(f, [12, 30], [0, 1], clamp);
  return (
    <Camera dur={s.dur} to={1.06}>
      <Bokeh />
      <Paper x={140} y={430} w={800} h={760} rot={-2} pop={0.85 + 0.15 * pop}>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <div style={{fontSize: 52, fontWeight: 800, letterSpacing: 2}}>{s.judulKartu ?? 'SURAT JALAN'}</div>
          <div style={{fontSize: 22, fontWeight: 700, padding: '6px 14px', border: `3px solid ${C.ink}`, borderRadius: 6}}>No. 0214</div>
        </div>
        <div style={{height: 4, background: C.ink, margin: '22px 0 30px'}} />
        {rows.map(([k, v], i) => (
          <div key={i} style={{display: 'flex', justifyContent: 'space-between', fontSize: 38, padding: '18px 0', borderBottom: '2px dashed rgba(13,27,36,0.25)', position: 'relative'}}>
            <span style={{opacity: 0.7}}>{k}</span>
            <span style={{fontWeight: 800, position: 'relative'}}>
              {v}
              {i === hi && (
                <svg width={300} height={110} style={{position: 'absolute', right: -40, top: -30, overflow: 'visible'}}>
                  <ellipse cx={150} cy={55} rx={140} ry={44} fill="none" stroke={C.orangeDeep} strokeWidth={6} strokeDasharray={600} strokeDashoffset={600 * (1 - circle)} transform="rotate(-4 150 55)" />
                </svg>
              )}
            </span>
          </div>
        ))}
        <div style={{position: 'absolute', bottom: 40, right: 50, transform: 'rotate(-10deg)', border: `5px solid ${C.mintDeep}`, color: C.mintDeep, fontWeight: 800, fontSize: 30, padding: '8px 18px', borderRadius: 8, opacity: 0.8}}>PT MAJU JAYA LOGISTIK</div>
      </Paper>
    </Camera>
  );
};

/* ---------- 3. TIMBANGAN: layar LED berat yang naik lalu berubah merah ---------- */
export const Timbangan: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const v = useCount(s.dari ?? 0, s.ke ?? 12, s.dur, 4, 0.55);
  const over = v > (s.batas ?? 8) + 0.01;
  const blink = over && Math.floor(f / 6) % 2 === 0;
  const col = over ? C.red : C.mint;
  return (
    <Camera dur={s.dur} from={1.04} to={1.12}>
      <AbsoluteFill style={{background: `radial-gradient(90% 60% at 50% 45%, #1a2c33 0%, ${C.night0} 80%)`}} />
      {/* dinding pos timbang */}
      <div style={{position: 'absolute', left: 90, top: 560, width: 900, height: 620, borderRadius: 26, background: 'linear-gradient(180deg,#22343b,#152328)', boxShadow: '0 40px 80px rgba(0,0,0,0.6)', border: '3px solid #2f474f'}} />
      <div style={{position: 'absolute', left: 150, top: 620, fontFamily: 'Outfit', fontWeight: 700, fontSize: 34, letterSpacing: 6, color: '#8fb4b0'}}>BERAT KENDARAAN</div>
      <div style={{position: 'absolute', left: 150, top: 690, width: 780, height: 330, borderRadius: 18, background: '#050a0c', border: '4px solid #0f1a1e', boxShadow: `inset 0 0 60px rgba(0,0,0,0.9), 0 0 ${over ? 80 : 40}px ${over ? 'rgba(255,90,90,0.35)' : 'rgba(127,240,214,0.18)'}`}}>
        <div style={{position: 'absolute', right: 60, top: 40, fontFamily: 'Outfit', fontWeight: 800, fontSize: 210, color: col, textShadow: `0 0 30px ${col}`, fontVariantNumeric: 'tabular-nums', letterSpacing: 4}}>{num(v, 2)}</div>
        <div style={{position: 'absolute', right: 66, bottom: 26, fontFamily: 'Outfit', fontWeight: 800, fontSize: 44, color: col, opacity: 0.9}}>TON</div>
      </div>
      <div style={{position: 'absolute', left: 150, top: 1050, padding: '14px 28px', borderRadius: 10, background: over ? C.red : '#20343a', color: over ? '#fff' : '#8fb4b0', fontFamily: 'Outfit', fontWeight: 800, fontSize: 38, letterSpacing: 4, opacity: over ? (blink ? 1 : 0.55) : 1}}>{over ? (s.peringatan ?? 'MELEBIHI BATAS') : 'MENIMBANG…'}</div>
      <div style={{position: 'absolute', right: 150, top: 1062, fontFamily: 'Outfit', fontWeight: 700, fontSize: 34, color: '#8fb4b0'}}>BATAS {num(s.batas ?? 8)} TON</div>
    </Camera>
  );
};

/* ---------- 4. STAT: kotak penghitung di peta gelap (gaya "7 → 150 NUCLEAR SILOS") ---------- */
export const Stat: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const v = useCount(s.dari ?? 0, s.ke ?? 50, s.dur, 4, 0.6);
  const fill = interpolate(v, [s.dari ?? 0, s.ke ?? 50], [0, 1], clamp);
  return (
    <Camera dur={s.dur} to={1.06}>
      <MapBg />
      {/* tumpukan muatan: batas (mint) dan kelebihan (merah) */}
      <div style={{position: 'absolute', left: 200, top: 520, width: 680, display: 'flex', flexDirection: 'column-reverse', gap: 10}}>
        {Array.from({length: 12}).map((_, i) => {
          const lim = i < 8;
          const show = lim || (i - 8) / 4 < fill;
          return <div key={i} style={{height: 46, borderRadius: 8, background: lim ? C.mintDeep : C.red, opacity: show ? (lim ? 0.85 : 0.95) : 0.08, boxShadow: !lim && show ? `0 0 24px ${C.red}` : 'none', transform: `scaleX(${show ? 1 : 0.9})`}} />;
        })}
      </div>
      <div style={{position: 'absolute', left: 200, top: 718, width: 680, borderTop: `5px dashed ${C.cream}`}} />
      <div style={{position: 'absolute', left: 200, top: 660, fontFamily: 'Outfit', fontWeight: 700, fontSize: 30, color: C.cream, letterSpacing: 3}}>BATAS</div>
      <Counter x={560} y={260} value={`+${num(v)}%`} label={s.label ?? 'KELEBIHAN MUATAN'} warn />
    </Camera>
  );
};

export const MapBg: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: `radial-gradient(110% 80% at 50% 40%, #0f2a40 0%, #081626 70%)`}}>
      <svg width={W} height={H} style={{position: 'absolute', opacity: 0.35}}>
        {Array.from({length: 18}).map((_, i) => (
          <path key={i} d={`M-50 ${120 + i * 110} C 300 ${80 + i * 110 + Math.sin(i) * 60}, 700 ${160 + i * 110 - Math.cos(i) * 50}, 1130 ${110 + i * 110}`} stroke="#2c5476" strokeWidth={1.5} fill="none" />
        ))}
        <path d="M540 0 L560 1920" stroke="#3b6a8f" strokeWidth={2} strokeDasharray="10 10" />
        <path d="M0 980 L1080 1010" stroke="#3b6a8f" strokeWidth={2} strokeDasharray="10 10" />
      </svg>
    </AbsoluteFill>
  );
};

export const Counter: React.FC<{x: number; y: number; value: string; label: string; warn?: boolean}> = ({x, y, value, label, warn}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame: f, fps, config: {damping: 13}});
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `scale(${pop})`, transformOrigin: 'left top', background: 'rgba(5,12,18,0.85)', border: `4px solid ${warn ? C.red : C.mint}`, borderRadius: 14, padding: '18px 28px', display: 'flex', alignItems: 'center', gap: 20, fontFamily: 'Outfit'}}>
      <div style={{width: 30, height: 30, background: warn ? C.red : C.mint, borderRadius: 4}} />
      <div>
        <div style={{fontSize: 96, fontWeight: 800, color: '#fff', lineHeight: 1, fontVariantNumeric: 'tabular-nums'}}>{value}</div>
        <div style={{fontSize: 24, fontWeight: 700, color: warn ? C.red : C.mint, letterSpacing: 3, marginTop: 6}}>{label}</div>
      </div>
    </div>
  );
};

/* ---------- 5. ATURAN: kartu aturan bergaya kertas ---------- */
export const Aturan: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame: f, fps, config: {damping: 11, stiffness: 140}});
  return (
    <Camera dur={s.dur} to={1.05}>
      <Bokeh />
      <Paper x={120} y={520} w={840} h={660} rot={1.5} pop={0.7 + 0.3 * pop}>
        <div style={{display: 'flex', justifyContent: 'center'}}>
          <div style={{background: C.orangeDeep, color: '#fff', fontWeight: 800, fontSize: 30, letterSpacing: 4, padding: '8px 22px', borderRadius: 6}}>ATURAN #{s.no ?? 1}</div>
        </div>
        <div style={{textAlign: 'center', fontSize: 70, fontWeight: 800, lineHeight: 1.08, margin: '30px 10px 26px', textTransform: 'uppercase', letterSpacing: -1}}>{s.judulKartu}</div>
        <div style={{height: 4, background: C.orangeDeep, margin: '0 60px'}} />
        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 46, marginTop: 34}}>
          <IconTruck />
          <div style={{fontSize: 80, fontWeight: 800, color: C.red}}>{s.ikonTengah ?? '✕'}</div>
          <IconBox />
        </div>
        {s.sumber && <div style={{position: 'absolute', bottom: 26, left: 40, right: 40, textAlign: 'center', fontSize: 22, opacity: 0.6}}>Sumber: {s.sumber}</div>}
      </Paper>
    </Camera>
  );
};
const IconTruck = () => (
  <svg width={150} height={90}><rect x={4} y={10} width={90} height={56} rx={6} fill={C.ink} /><path d="M98 30 h28 l20 22 v14 h-48z" fill={C.ink} /><circle cx={30} cy={74} r={12} fill={C.ink} /><circle cx={120} cy={74} r={12} fill={C.ink} /></svg>
);
const IconBox = () => (
  <svg width={110} height={90}><rect x={6} y={30} width={50} height={50} fill={C.orangeDeep} /><rect x={54} y={30} width={50} height={50} fill={C.orange} /><rect x={30} y={0} width={50} height={32} fill={C.orangeDeep} opacity={0.8} /></svg>
);

/* ---------- 6. KARAKTER: Sopir/Bos di lokasi malam ---------- */
export const Karakter: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const who = s.siapa ?? 'sopir';
  const set = s.set ?? 'timbang';
  return (
    <Camera dur={s.dur} to={1.09} oy="50%" pan={-20}>
      {set === 'kantor' ? <Kantor /> : (
        <>
          <NightSky horizon={1150} warm={0.8} />
          <svg width={W} height={H} style={{position: 'absolute'}}>
            <rect x={0} y={1150} width={W} height={770} fill="#132228" />
            <rect x={0} y={1560} width={W} height={12} fill="#24393f" />
          </svg>
          <Truck x={-470} y={1180} s={1.1} lights={false} />
          <Lamp x={880} y={620} h={680} s={1} />
          {s.kardus && (
            <div style={{position: 'absolute', left: 120, top: 1470}}>
              {[0, 1, 2, 3, 4].map((i) => (
                <div key={i} style={{position: 'absolute', left: (i % 3) * 120, top: -Math.floor(i / 3) * 100 + (i > 2 ? 0 : 0) - (i >= 3 ? 100 : 0), width: 110, height: 96, background: i % 2 ? '#c48b52' : '#b07a45', border: '3px solid #8a5a2e', borderRadius: 4}} />
              ))}
            </div>
          )}
        </>
      )}
      <Person who={who} x={s.x ?? 520} y={s.y ?? 880} s={s.skala ?? 1.15} pose={s.pose ?? 'cemas'} face={s.hadap ?? -1} />
    </Camera>
  );
};

const Kantor: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, #0b1d24 0%, #0f262e 100%)`}}>
      {/* jendela malam dengan lampu kota */}
      <div style={{position: 'absolute', left: 90, top: 300, width: 900, height: 700, borderRadius: 12, background: 'linear-gradient(180deg,#081521,#14303c)', border: '14px solid #1b333b', overflow: 'hidden'}}>
        {Array.from({length: 40}).map((_, i) => {
          const x = random(`kx${i}`) * 880, y = 380 + random(`ky${i}`) * 300, r = 6 + random(`kr${i}`) * 16;
          return <div key={i} style={{position: 'absolute', left: x, top: y, width: r, height: r, borderRadius: '50%', background: i % 3 ? 'rgba(255,190,120,0.6)' : 'rgba(127,240,214,0.5)', filter: 'blur(2px)'}} />;
        })}
        <div style={{position: 'absolute', left: 440, top: 0, width: 14, height: 700, background: '#1b333b'}} />
      </div>
      {/* lampu meja */}
      <div style={{position: 'absolute', left: 640, top: 1080, width: 520, height: 520, borderRadius: '50%', background: 'radial-gradient(circle, rgba(255,200,140,0.35) 0%, transparent 65%)'}} />
      <div style={{position: 'absolute', left: 0, top: 1480, width: W, height: 440, background: 'linear-gradient(180deg,#3a2a22,#24180f)'}} />
      <div style={{position: 'absolute', left: 0, top: 1480, width: W, height: 16, background: '#5a4334'}} />
    </AbsoluteFill>
  );
};

/* ---------- 7. PETA: rute dengan penanda KAMU dan trip tambahan ---------- */
export const Peta: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const d1 = interpolate(f, [0, s.dur * 0.35], [0, 1], {...clamp, easing: easeOut});
  const d2 = interpolate(f, [s.dur * 0.3, s.dur * 0.85], [0, 1], {...clamp, easing: easeOut});
  const path = 'M220 1560 C 360 1340, 420 1060, 560 940 S 800 700, 860 560';
  const trips = Math.round(interpolate(f, [s.dur * 0.3, s.dur * 0.6], [s.tripDari ?? 1, s.tripKe ?? 2], clamp));
  return (
    <Camera dur={s.dur} to={1.08} oy="50%">
      <MapBg />
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <path d="M80 1500 C 200 1300, 300 1100, 520 960 S 900 700, 1000 380" stroke="#24476a" strokeWidth={90} fill="none" opacity={0.35} strokeLinecap="round" />
        <text x={300} y={1640} fontFamily="Outfit" fontWeight={700} fontSize={30} fill="#7ea4c4" letterSpacing={6}>{s.provDari ?? 'SUMATERA SELATAN'}</text>
        <text x={640} y={470} fontFamily="Outfit" fontWeight={700} fontSize={30} fill="#7ea4c4" letterSpacing={6}>{s.provKe ?? 'JAMBI'}</text>
        <path d={path} stroke="#ffffff" strokeWidth={8} fill="none" strokeLinecap="round" strokeDasharray={1400} strokeDashoffset={1400 * (1 - d1)} style={{filter: 'drop-shadow(0 0 10px rgba(255,255,255,0.6))'}} />
        <path d={path} stroke={C.orange} strokeWidth={8} fill="none" strokeLinecap="round" strokeDasharray="22 18" transform="translate(26 18)" opacity={d2 > 0 ? 1 : 0} style={{clipPath: `inset(${(1 - d2) * 100}% 0 0 0)`}} />
        {[[220, 1560, s.dari ?? 'PALEMBANG'], [860, 560, s.ke ?? 'JAMBI']].map(([x, y, n]: any, i) => (
          <g key={i}>
            <circle cx={x} cy={y} r={16} fill="#fff" />
            <circle cx={x} cy={y} r={30} fill="none" stroke="#fff" strokeWidth={3} opacity={0.5 + 0.5 * Math.sin(f / 5)} />
            <rect x={x + (i ? -250 : 30)} y={y - 30} width={220} height={52} rx={26} fill="#fff" />
            <text x={x + (i ? -140 : 140)} y={y + 6} textAnchor="middle" fontFamily="Outfit" fontWeight={800} fontSize={28} fill={C.ink}>{n}</text>
          </g>
        ))}
      </svg>
      <div style={{position: 'absolute', left: 150, top: 1600, background: C.mint, color: C.ink, fontFamily: 'Outfit', fontWeight: 800, fontSize: 30, padding: '6px 18px', borderRadius: 20}}>KAMU</div>
      <Counter x={560} y={240} value={`${trips}×`} label={s.label ?? 'TRIP KE JAMBI'} warn={trips > (s.tripDari ?? 1)} />
    </Camera>
  );
};

/* ---------- 8. STRUK: rincian biaya yang muncul satu-satu, total naik ---------- */
export const Struk: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const items: [string, number][] = s.item ?? [];
  const per = (s.dur * 0.6) / Math.max(1, items.length);
  const shown = items.filter((_, i) => f > 6 + i * per);
  const total = shown.reduce((a, [, v]) => a + v, 0);
  const pop = spring({frame: f, fps, config: {damping: 15}});
  return (
    <Camera dur={s.dur} to={1.05}>
      <Bokeh tint="rgba(127,240,214," />
      <div style={{position: 'absolute', left: 190, top: 380, width: 700, transform: `translateY(${(1 - pop) * 120}px) rotate(-1.5deg)`, fontFamily: 'Outfit', color: C.ink}}>
        <div style={{background: C.cream, padding: '44px 46px 30px', boxShadow: '0 30px 60px rgba(0,0,0,0.55)'}}>
          <div style={{textAlign: 'center', fontWeight: 800, fontSize: 44, letterSpacing: 3}}>{s.judulKartu ?? 'BIAYA TRIP TAMBAHAN'}</div>
          <div style={{textAlign: 'center', fontSize: 24, opacity: 0.6, marginTop: 6}}>{s.subjudul ?? 'Palembang → Jambi PP · Fuso'}</div>
          <div style={{borderTop: '3px dashed rgba(13,27,36,0.4)', margin: '26px 0 10px'}} />
          {items.map(([k, v], i) => (
            <div key={i} style={{display: 'flex', justifyContent: 'space-between', fontSize: 38, padding: '14px 0', opacity: f > 6 + i * per ? 1 : 0.12, transform: `translateX(${f > 6 + i * per ? 0 : -20}px)`}}>
              <span>{k}</span><span style={{fontWeight: 700, fontVariantNumeric: 'tabular-nums'}}>{rp(v)}</span>
            </div>
          ))}
          <div style={{borderTop: `4px solid ${C.ink}`, margin: '16px 0 0', paddingTop: 18, display: 'flex', justifyContent: 'space-between', fontSize: 50, fontWeight: 800}}>
            <span>TOTAL</span><span style={{color: C.orangeDeep, fontVariantNumeric: 'tabular-nums'}}>{rp(total)}</span>
          </div>
          {s.catatan && <div style={{fontSize: 20, opacity: 0.55, marginTop: 14}}>{s.catatan}</div>}
        </div>
        <svg width={700} height={26} style={{display: 'block'}}><path d={'M0 0 ' + Array.from({length: 28}).map((_, i) => `L${i * 25 + 12.5} 22 L${(i + 1) * 25} 0`).join(' ') + ' Z'} fill={C.cream} /></svg>
      </div>
    </Camera>
  );
};

/* ---------- 9. ANGKA BESAR: untung berubah jadi rugi ---------- */
export const AngkaBesar: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const v = useCount(s.dari ?? 0, s.ke ?? 0, s.dur, 8, 0.6);
  const neg = v < 0;
  const col = neg ? C.red : C.mint;
  const shake = neg ? Math.sin(f * 2.2) * 3 * interpolate(f, [s.dur * 0.6, s.dur * 0.8], [1, 0], clamp) : 0;
  return (
    <Camera dur={s.dur} to={1.06}>
      <AbsoluteFill style={{background: `radial-gradient(80% 50% at 50% 45%, ${neg ? 'rgba(255,90,90,0.18)' : 'rgba(127,240,214,0.14)'} 0%, ${C.night0} 75%)`}} />
      <div style={{position: 'absolute', top: 560, width: '100%', textAlign: 'center', fontFamily: 'Outfit', fontWeight: 700, fontSize: 40, letterSpacing: 6, color: '#9fbfbb'}}>{s.label ?? 'UNTUNG ORDER INI'}</div>
      <div style={{position: 'absolute', top: 640, width: '100%', textAlign: 'center', fontFamily: 'Outfit', fontWeight: 800, fontSize: 150, color: col, textShadow: `0 0 40px ${col}66`, transform: `translateX(${shake}px)`, fontVariantNumeric: 'tabular-nums', letterSpacing: -2}}>{rp(v)}</div>
      <svg width={W} height={300} style={{position: 'absolute', top: 860}}>
        <path d={`M540 40 L540 ${120 + 80 * interpolate(f, [8, s.dur * 0.6], [0, 1], clamp)}`} stroke={col} strokeWidth={14} strokeLinecap="round" />
        <path d={`M490 ${150 + 80 * interpolate(f, [8, s.dur * 0.6], [0, 1], clamp) - 50} l50 50 l50 -50`} stroke={col} strokeWidth={14} fill="none" strokeLinecap="round" strokeLinejoin="round" opacity={neg ? 1 : 0.3} />
      </svg>
      {s.catatan && <div style={{position: 'absolute', top: 1160, width: '100%', textAlign: 'center', fontFamily: 'Outfit', fontSize: 26, color: '#6f8f8b'}}>{s.catatan}</div>}
    </Camera>
  );
};

/* ---------- 10. CTA: hantu Ghostrip + ajakan ---------- */
export const Cta: React.FC<{s: SceneSpec}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame: f, fps, config: {damping: 10}});
  const pill = spring({frame: f - 10, fps, config: {damping: 12}});
  return (
    <AbsoluteFill style={{background: `radial-gradient(90% 60% at 50% 38%, #12404a 0%, ${C.night0} 75%)`}}>
      <div style={{position: 'absolute', left: 340, top: 260 + Math.sin(f / 9) * 14, width: 400, height: 400, borderRadius: '50%', background: 'radial-gradient(circle, rgba(127,240,214,0.35) 0%, transparent 70%)'}} />
      <Img src={staticFile('ghost_wave.png')} style={{position: 'absolute', left: 400, top: 300 + Math.sin(f / 9) * 14, width: 280, transform: `scale(${pop}) rotate(${Math.sin(f / 12) * 6}deg)`, filter: 'drop-shadow(0 0 40px rgba(127,240,214,0.6))'}} />
      <div style={{position: 'absolute', top: 640, width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 22, transform: `scale(${pop})`}}>
        <Img src={staticFile('icon.png')} style={{width: 110, height: 110, borderRadius: 26}} />
        <div style={{fontFamily: 'Outfit', fontWeight: 800, fontSize: 84, color: '#fff'}}>Ghostrip</div>
      </div>
      <div style={{position: 'absolute', top: 800, width: '100%', textAlign: 'center', fontFamily: 'Outfit', fontWeight: 600, fontSize: 46, color: '#cfe9e4', padding: '0 90px', boxSizing: 'border-box', lineHeight: 1.25}}>{s.tagline ?? 'Hitung harga trip yang aman, sebelum truk berangkat'}</div>
      <div style={{position: 'absolute', top: 990, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <div style={{transform: `scale(${pill})`, background: C.orange, color: '#1a0e05', fontFamily: 'Outfit', fontWeight: 800, fontSize: 56, padding: '22px 54px', borderRadius: 999, boxShadow: '0 16px 50px rgba(255,157,92,0.45)'}}>GRATIS 7 HARI</div>
      </div>
      <div style={{position: 'absolute', top: 1140, width: '100%', textAlign: 'center', fontFamily: 'Outfit', fontWeight: 800, fontSize: 52, color: C.mint}}>Komen DEMO untuk coba</div>
      <div style={{position: 'absolute', top: 1220, width: '100%', textAlign: 'center', fontFamily: 'Outfit', fontWeight: 600, fontSize: 32, color: '#8fb4b0'}}>WA 0815-1704-7930</div>
    </AbsoluteFill>
  );
};

export const SCENES: Record<string, React.FC<{s: SceneSpec}>> = {
  jalan: Jalan, dokumen: Dokumen, timbangan: Timbangan, stat: Stat, aturan: Aturan,
  karakter: Karakter, peta: Peta, struk: Struk, angka: AngkaBesar, cta: Cta,
};
