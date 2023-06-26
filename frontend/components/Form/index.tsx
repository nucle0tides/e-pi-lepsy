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
