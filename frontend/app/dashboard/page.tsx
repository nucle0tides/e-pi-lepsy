import { AddPetForm } from "@/components/Form";

interface Pet {
  publicId: string;
  firstName: string;
  lastName: string;
  householdId: number;
}

export default async function Dashboard() {
  const pets: Pet[] = await fetch("http://localhost:3000/api/pet/list")
    .then((res) => res.json())
    .catch((error) => console.error(error));
  return (
    <>
      <div className="flex flex-wrap">
        <h1 className="basis-full text-neutral-200">$NAME HOUSEHOLD</h1>
        <div className="min-h-screen basis-full bg-neutral-200">
          <div className="flex">
            <div>
              <h2>Pet List</h2>
              <ul>
                {pets.map((x, i) => (
                  <li key={i}>{x.firstName}</li>
                ))}
              </ul>
              <h2>create new pet</h2>
              <AddPetForm />
            </div>
            <div>
              <p>CALENDAR GOES HERE LOL</p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
