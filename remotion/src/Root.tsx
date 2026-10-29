import React, {useState} from 'react';
import {
  AbsoluteFill, Audio, Composition, Sequence, continueRender, delayRender, interpolate,
  spring, staticFile, useCurrentFrame, useVideoConfig,
} from 'remotion';
import {C, FPS, H, W, WhatIfProps} from './theme';
import {SCENES} from './scenes';
import {Grain, clamp} from './parts';

const useOutfit = () => {
  const [h] = useState(() => delayRender('font'));
  React.useEffect(() => {
    const f = new FontFace('Outfit', `url(${staticFile('Outfit.ttf')})`, {weight: '100 900'});
    f.load().then((ff) => { (document.fonts as any).add(ff); continueRender(h); });
  }, [h]);
};

// Teks besar per frasa di tengah bawah; kata di dalam *bintang* diberi warna oranye
const Caption: React.FC<{text: string; dur: number}> = ({text, dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame: f, fps, config: {damping: 14, stiffness: 220}});
  const out = interpolate(f, [dur - 3, dur], [1, 0.0], clamp);
  const parts = text.split(/(\*[^*]+\*)/g).filter(Boolean);
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: 1330, textAlign: 'center', opacity: out, transform: `scale(${1.12 - 0.12 * pop})`}}>
      <span style={{fontFamily: 'Outfit', fontWeight: 900, fontSize: 84, lineHeight: 1.08, letterSpacing: -1.5, textTransform: 'uppercase', color: '#fff',
        textShadow: '0 5px 0 rgba(0,0,0,0.55), 0 0 26px rgba(0,0,0,0.75), 0 0 2px #000'}}>
        {parts.map((p, i) => p.startsWith('*') ? <span key={i} style={{color: C.orange}}>{p.slice(1, -1)}</span> : <span key={i}>{p}</span>)}
      </span>
    </div>
  );
};

const TitleCard: React.FC<{judul: string; part: number; lokasi: string; seri?: string}> = ({judul, part, lokasi, seri}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame: f, fps, config: {damping: 14}});
  const b = spring({frame: f - 6, fps, config: {damping: 14}});
  return (
    <div style={{position: 'absolute', top: 250, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16, fontFamily: 'Outfit'}}>
      <div style={{transform: `scale(${a})`, background: C.orangeDeep, color: '#fff', fontWeight: 800, fontSize: 36, letterSpacing: 2, padding: '10px 26px', borderRadius: 8, boxShadow: '0 10px 30px rgba(0,0,0,0.5)', textAlign: 'center', maxWidth: 900}}>
        {(seri ?? 'GIMANA KALAU…')} {judul}{part ? ` · PART ${part}` : ''}
      </div>
      <div style={{transform: `scale(${b})`, background: C.cream, color: C.ink, fontWeight: 700, fontSize: 28, padding: '8px 22px', borderRadius: 999, display: 'flex', alignItems: 'center', gap: 10}}>
        <span style={{width: 18, height: 18, borderRadius: '50%', background: C.orange, display: 'inline-block'}} />{lokasi}
      </div>
    </div>
  );
};

// Label jam berjalan (seperti "18:51" di referensi)
const Clock: React.FC<{start: string; minutesPerScene: number; index: number}> = ({start, minutesPerScene, index}) => {
  const f = useCurrentFrame();
  const [hh, mm] = start.split(':').map(Number);
  const t = hh * 60 + mm + index * minutesPerScene + Math.floor(f / 20);
  const s = `${String(Math.floor(t / 60) % 24).padStart(2, '0')}:${String(t % 60).padStart(2, '0')}`;
  return (
    <div style={{position: 'absolute', left: 50, top: 250, display: 'flex', alignItems: 'center', gap: 12, background: 'rgba(30,8,8,0.8)', border: `3px solid ${C.red}`, borderRadius: 999, padding: '8px 20px', fontFamily: 'Outfit', fontWeight: 800, fontSize: 34, color: '#fff', fontVariantNumeric: 'tabular-nums'}}>
      <span style={{width: 16, height: 16, borderRadius: '50%', background: C.red, boxShadow: `0 0 12px ${C.red}`}} />{s} WIB
    </div>
  );
};

export const WhatIf: React.FC<WhatIfProps> = (p) => {
  useOutfit();
  return (
    <AbsoluteFill style={{background: C.night0}}>
      {p.scenes.map((s, i) => {
        const Comp = SCENES[s.type] ?? SCENES.angka;
        return (
          <Sequence key={i} from={s.from} durationInFrames={s.dur}>
            <Comp s={s} />
            {i === 0 && <TitleCard judul={p.judul} part={p.part} lokasi={p.lokasi} seri={(p as any).seri} />}
            {i > 0 && s.type !== 'cta' && s.type !== 'logo' && p.jam && <Clock start={p.jam} minutesPerScene={3} index={i} />}
            {s.type !== 'cta' && s.type !== 'logo' && s.chunks.map((c, j) => (
              <Sequence key={j} from={c.from} durationInFrames={Math.max(1, c.to - c.from)}>
                <Caption text={c.text} dur={Math.max(1, c.to - c.from)} />
              </Sequence>
            ))}
            {p.whoosh && i > 0 && <Audio src={staticFile(p.whoosh)} volume={0.35} />}
          </Sequence>
        );
      })}
      <Grain />
      <div style={{position: 'absolute', left: 40, top: 150, background: 'rgba(0,0,0,0.45)', color: '#e9f5f3', fontFamily: 'Outfit', fontWeight: 600, fontSize: 26, padding: '6px 16px', borderRadius: 8}}>{p.handle}</div>
      {p.narasi && <Sequence from={6}><Audio src={staticFile(p.narasi)} /></Sequence>}
      {p.musik && <Audio src={staticFile(p.musik)} volume={p.narasi ? 0.22 : 0.55} />}
    </AbsoluteFill>
  );
};

const contoh: WhatIfProps = {
  judul: 'CONTOH', part: 1, lokasi: '02.14 WIB · JALINTIM SUMATERA', jam: '02:14', handle: '@ghostrip.app',
  durationInFrames: 90, narasi: null, musik: null, whoosh: null,
  scenes: [{type: 'jalan', from: 0, dur: 90, narasi: 'Contoh', chunks: [{text: 'CONTOH *ADEGAN*', from: 0, to: 90}]}],
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="WhatIf"
    component={WhatIf as any}
    durationInFrames={90}
    fps={FPS}
    width={W}
    height={H}
    defaultProps={contoh}
    calculateMetadata={({props}) => ({durationInFrames: (props as WhatIfProps).durationInFrames})}
  />
);
