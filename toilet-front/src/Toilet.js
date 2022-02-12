import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

const Toilet = () => {
  const [detail, setDetail] = useState()
  const { roomID } = useParams()

  useEffect(() => {
    RoomStatus(roomID).then((data) => {
      setDetail(Object.entries(data))
      console.log(data)
    })
  }, [roomID])

  async function RoomStatus(id) {
  // var config = {
  //   headers: {'Access-Control-Allow-Origin': '*'}
  // };
  const res = await axios.get(
    `https://ecourse.cpe.ku.ac.th/exceed03/api/room-status/1`
    )
    return res.data
  }

  return (
    <div>
      { detail }
    </div>
  )
}
export default Toilet;