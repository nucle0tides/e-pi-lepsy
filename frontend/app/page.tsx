import Link from "next/link";

export default async function Index() {
  return (
    <>
      <div className="flex flex-wrap">
        <h1 className="basis-full text-neutral-200">e-pi-lepsy</h1>
        <div className="min-h-screen basis-full bg-neutral-200">
          <div className="flex content-center justify-center">
            <Link className="m-20 text-2xl" href="/dashboard">
              Dashboard
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
