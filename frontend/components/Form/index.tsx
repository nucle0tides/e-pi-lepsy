"use client";

import { useForm, SubmitHandler } from "react-hook-form";

type AddPetInputs = {
  firstName: string;
  lastName: string;
  householdId: number;
  dateOfBirth: string;
};

export function AddPetForm() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<AddPetInputs>();
  const onSubmit: SubmitHandler<AddPetInputs> = (data) => console.log(data);

  console.log(watch("firstName")); // watch input value by passing the name of it

  return (
    /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
    <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 gap-6">
      {/* register your input into the hook by invoking the "register" function */}
      {/* include validation with required or other standard HTML validation rules */}
      <label>
        <span className="">first name</span>
        <input type="text" {...register("firstName", { required: true })} />
      </label>
      { errors.firstName && <span className="text-red-500">This field is required</span> }
      <label className="block">
        <span>last name</span>
        <input type="text" {...register("lastName", { required: true })} />
      </label>
      { errors.lastName && <span className="text-red-500">This field is required</span> }
      <label className="block">
        <span>household ID</span>
        <input type="text" {...register("householdId", { required: true })} />
      </label>
      { errors.householdId && <span className="text-red-500">This field is required</span> }
      <label className="block">
        <span>date of birth (YY-mm-dd)</span>
        <input type="text" {...register("dateOfBirth", { required: true })} />
      </label>
      { errors.dateOfBirth && <span className="text-red-500">This field is required</span> }
      {/* errors will return when field validation fails  */}
      {/* TODO: hilariously bad error checking */}
      <label className="block">
        <span className="px-4 py-1 text-sm text-purple-600 font-semibold rounded-full border border-purple-200 hover:text-white hover:bg-purple-600 hover:border-transparent focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2">submit</span>
        <button type="submit"></button>
      </label>
    </form>
  );
}

type SeizureLogInputs = {
  petId: string;
  date: Date;
  seizureType: "FOCAL" | "TONICCLONIC" | "UNSPECIFIED"
  episodeStart: Date;
  episodeEnd: Date;
  seizureStart?: Date;
  seizureEnd?: Date;
  isClusterEvent?: boolean;
  location?: string;
  notes?: string;
  medicationAdministered?: string;
  medicationDosage?: string;
};

export function SeizureLogForm() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<SeizureLogInputs>();
  
  const onSubmit: SubmitHandler<SeizureLogInputs> = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 gap-6">
      {/* register your input into the hook by invoking the "register" function */}
      {/* include validation with required or other standard HTML validation rules */}
      <label>
        <span>pet ID</span>
        <input type="text" {...register("petId", { required: true })} />
      </label>
      { errors.petId && <span className="text-red-500">This field is required</span> }
      <label className="block">
        <span>date of activity</span>
        <input type="date" {...register("date", { required: true })} />
      </label>
      { errors.date && <span className="text-red-500">This field is required</span> }
      <label className="block">
        <span>seizure type</span>
        <select id="s-type" {...register("seizureType", {required: true})}>
          <option value="FOCAL">Focal</option>
          <option value="TONICCLONIC">Tonic Clonic</option>
          <option value="UNSPECIFIED">Unspecified</option>
        </select>
      </label>
      { errors.seizureType && <span className="text-red-500">This field is required</span> }
      <label className="block">
        <span>start of episode</span>
        <input type="datetime-local" {...register("episodeStart", { required: true })} />
      </label>
      { errors.episodeStart && <span className="text-red-500">This field is required</span> }
      <label className="block">
        <span>end of episode</span>
        <input type="datetime-local" {...register("episodeEnd", { required: true })} />
      </label>
      { errors.episodeEnd && <span className="text-red-500">This field is required</span> }
      <label className="block">
        <span>start of seizures</span>
        <input type="datetime-local" {...register("seizureStart", { required: false })} />
      </label>
      <label className="block">
        <span>end of seizures</span>
        <input type="datetime-local" {...register("seizureEnd", { required: false })} />
      </label>
      <fieldset>
        <legend>cluster event?</legend>
        <label className="block">
          <span>false</span>
          <input type="radio" checked value="false" {...register("isClusterEvent", { required: false })} />
        </label>
        <label className="block">
          <span>true</span>
          <input type="radio" value="true" {...register("isClusterEvent", { required: false })} />
        </label>
      </fieldset>
      <label>
        <span className="">location?</span>
        <input type="text" {...register("location", { required: false })} />
      </label>
      <label>
        <span className="">notes?</span>
        <input type="text" {...register("notes", { required: false })} />
      </label>
      <label>
        <span className="">medication administered?</span>
        <input type="text" {...register("medicationAdministered", { required: false })} />
      </label>
      <label>
        <span className="">medication dosage?</span>
        <input type="text" {...register("medicationAdministered", { required: false })} />
      </label>
      {/* errors will return when field validation fails  */}
      {/* TODO: hilariously bad error checking */}
      <label className="block">
        <span className="px-4 py-1 text-sm text-purple-600 font-semibold rounded-full border border-purple-200 hover:text-white hover:bg-purple-600 hover:border-transparent focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2">submit</span>
        <button type="submit"></button>
      </label>
    </form>
  );
}