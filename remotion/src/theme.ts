// Palet brand Ghostrip untuk gaya "Gimana kalau…" (sinematik malam, aksen oranye & mint)
export const C = {
  night0: '#040d13',
  night1: '#071a22',
  night2: '#0b2733',
  teal: '#0f3b46',
  tealSoft: '#1d5a63',
  mint: '#7ff0d6',
  mintDeep: '#2fb8a0',
  orange: '#ff9d5c',
  orangeDeep: '#e2733a',
  glow: '#ffb27a',
  cream: '#f2ead9',
  creamShade: '#ddd2bc',
  ink: '#0d1b24',
  red: '#ff5a5a',
  skin: '#f1c69a',
  skinShade: '#d9a674',
  steel: '#33505a',
  steelDark: '#203841',
  asphalt: '#16262d',
};

export const FPS = 30;
export const W = 1080;
export const H = 1920;

export type CaptionChunk = {text: string; from: number; to: number};
export type SceneSpec = {
  type: string;
  from: number; // frame mulai
  dur: number; // jumlah frame
  narasi: string;
  chunks: CaptionChunk[];
  [k: string]: any;
};
export type WhatIfProps = {
  judul: string; // judul seri, mis. "TRUK DITAHAN DI JEMBATAN TIMBANG"
  part: number;
  lokasi: string; // "02.14 WIB · JALINTIM SUMATERA"
  jam?: string; // jam awal untuk label jam berjalan, "02:14"
  scenes: SceneSpec[];
  durationInFrames: number;
  narasi?: string | null; // file audio narasi di public/
  musik?: string | null;
  whoosh?: string | null;
  handle: string;
};
