import React from 'react'
import numeral from 'numeral'

export default function DisplayCount(props) {
    return <span className={props.className}>{numeral(props.children).format("0a")}</span>

}
