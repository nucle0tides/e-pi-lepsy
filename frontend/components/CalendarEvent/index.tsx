export default function CalendarEvent({ petName, summary, date } : { petName: string, summary: string, date: string }) {
  return (
    <div className="flex gap-4 w-full bg-violet-200 mt-1 mb-1 rounded p-1 items-center">
      <p>{petName}</p>
      <div className="flex flex-col">
        <p>{summary}</p>
        <p className="text-gray-500 text-sm">{date}</p>
      </div>
    </div>
  )
}