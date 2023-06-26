'use client';

// NOTE: personal note, this library Just Worked with the most minimal setup but pulls in date-fns whereas
//       @wojtekmaj/react-calendar pulls in no date lib dependencies and can still be styled in a fairly sane manner.
//       Something to consider if date-fns becomes undesirable.

import { ClassNames, DayPicker } from "react-day-picker";
import styles from 'react-day-picker/dist/style.module.css';
import * as myStyles from './Calendar.module.css';
import CalendarEvent from "../CalendarEvent";

// TODO: Might be that a single calendar component will work for both household summaries and individual pets but
//       otherwise should break out a few calendar components, eg
//       - "Dashboard Calendar" takes the meta info for all pets of a household and give a summary of all events
//       - "Pet Calendar" takes the meta info for only a single pet gives a summary of all events for that specific pet
export default function Calendar() {

  const days = [new Date(2023, 5, 24), new Date(2023, 5, 3)];

  const classNames : ClassNames = {
    ...styles,
    // @ts-ignore
    root: myStyles.root,
    // @ts-ignore
    day_selected: myStyles.my_selected,
    // @ts-ignore    
    month: myStyles.my_month,
    // @ts-ignore
    table: myStyles.my_table,
  };

  const dummyEvents = [{ petName: "pius", summary: "im baby.", date: "2023.06.03"}, {petName: "smalls", date: "2023.06.24", summary: "i will consume the world."}]


  return (
    <div className="flex flex-col w-full">
      <div className="w-5/6">
        <DayPicker
          classNames={classNames}
          mode="multiple"
          selected={days}
        />
      </div>
      <div className="mt-5 w-4/5">
            <h2 className="text-md font-semibold">Upcoming</h2>
            <CalendarEvent {...dummyEvents[0]} />
            <CalendarEvent {...dummyEvents[1]} />
      </div>
    </div>
  )
}