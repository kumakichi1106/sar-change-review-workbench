const sceneBasePath = `${import.meta.env.BASE_URL}data/scenes/yokohama-sentinel-1`;

const imagePanels = [
  { title: "Before", src: `${sceneBasePath}/before.png` },
  { title: "After", src: `${sceneBasePath}/after.png` },
  { title: "Diff", src: `${sceneBasePath}/diff.png` },
  { title: "Mask", src: `${sceneBasePath}/mask.png` },
];

export default function App() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto w-full max-w-6xl px-5 py-10">
        <h1 className="max-w-4xl text-3xl font-bold leading-tight md:text-4xl">
          横浜市中区、西区、神奈川区周辺 Sentinel-1 簡易比較
        </h1>

        <p className="mt-5 max-w-3xl leading-8 text-slate-600">
          宙畑の記事を参考に、行政区域データから横浜市周辺を抽出し、
          Sentinel-1 GRD画像を取得・可視化しました。ここでは取得画像をもとに、
          Pythonで生成した簡易差分を表示しています。
        </p>

        <section className="mt-6 rounded-lg border-l-4 border-teal-600 bg-teal-50 p-4 leading-7 text-teal-950">
          本アプリは本番レベルのSAR解析ツールではありません。画像ベースの簡易差分を用いて、
          SAR由来データをWeb UIで確認・比較する流れを学ぶためのプロトタイプです。
        </section>

        <section className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-2">
          {imagePanels.map((panel) => (
            <figure
              key={panel.title}
              className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm"
            >
              <figcaption className="border-b border-slate-200 px-4 py-3 font-bold">
                {panel.title}
              </figcaption>
              <img
                src={panel.src}
                alt={`${panel.title} SAR view`}
                className="block w-full bg-slate-950"
              />
            </figure>
          ))}
        </section>
      </div>
    </main>
  );
}