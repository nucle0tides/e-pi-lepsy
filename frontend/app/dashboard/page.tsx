import { AddPetForm, SeizureLogForm } from "@/components/Form";
import Calendar from "@/components/Calendar";
import { QuickSchedule } from "@/components/Buttons";

interface Pet {
  publicId: string;
  firstName: string;
  lastName: string;
  householdId: number;
  dateOfBirth: string;
}

export default async function Dashboard() {
  const pets: Pet[] = await fetch("http://localhost:3000/api/pet/list")
    .then((res) => res.json())
    .catch((error) => console.error(error));
  return (
    <>
      <div className="flex flex-wrap bg-indigo-900 pl-1 pr-1">
        <div className="basis-full h-8 flex items-center ml-2 mr-2">
          <p className="text-neutral-200">$NAME HOUSEHOLD</p>
        </div>
        <div className="min-h-screen basis-full bg-neutral-200 rounded">
          <div className="flex m-3">
            <div className=" w-3/5">
              <h2 className="text-lg font-bold mt-1 mb-2">Hello, $HOUSEHOLD</h2>
              <h3 className="text-md font-bold mb-2">Overview</h3>
              <ul>
                  {pets.map((x, i) => (
                    <li key={i}>
                      <div className="flex flex-wrap items-center bg-neutral-50 rounded w-3/4 h-12 mt-1 mb-1 p-1">
                          <p className="basis-1/2">{x.firstName} {x.lastName}</p>
                          <p className="basis-1/2">{x.dateOfBirth}</p>
                      </div>
                    </li>
                  ))}
              </ul>
              <h2 className="text-lg font-bold mt-2 mb-2">New family member? Add them them to your household</h2>
              <div className="bg-neutral-50 rounded w-8/12 p-1">
                <AddPetForm />
              </div>
              <h2 className="text-lg font-bold mt-2 mb-2">New seizure activity? log it</h2>
              <div className="bg-neutral-50 rounded w-8/12 p-1">
                <SeizureLogForm/>
              </div>
            </div>
            <div className="flex flex-col w-2/5">
              <Calendar/>
              <div className="w-4/5 mt-2">
                <QuickSchedule/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
